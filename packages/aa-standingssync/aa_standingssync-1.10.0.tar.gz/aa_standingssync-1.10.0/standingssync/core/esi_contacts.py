"""Core logic for handling ESI contacts."""

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass, field, fields
from enum import Enum
from typing import Any, Dict, FrozenSet, Iterable, List, Optional, Set, Tuple

from eveuniverse.models import EveEntity

from standingssync.app_settings import STANDINGSSYNC_WAR_TARGETS_LABEL_NAME


@dataclass(frozen=True)
class EsiContactLabel:
    """An ESI contact label. Immutable."""

    id: int
    name: str

    def __post_init__(self):
        object.__setattr__(self, "id", int(self.id))
        object.__setattr__(self, "name", str(self.name))

    def to_dict(self) -> dict:
        """Return as dict."""
        return {self.id: self.name}

    def to_esi_dict(self) -> dict:
        """Return as dict in ESI format."""
        return {"label_id": self.id, "label_name": self.name}

    @classmethod
    def from_esi_dict(cls, esi_dict: dict) -> "EsiContactLabel":
        """Create new obj from ESI dict."""
        return cls(id=esi_dict["label_id"], name=esi_dict["label_name"])


@dataclass(frozen=True)
class EsiContact:
    """An ESI contact. Immutable."""

    class ContactType(str, Enum):
        """A contact type."""

        ALLIANCE = "alliance"
        CHARACTER = "character"
        CORPORATION = "corporation"
        FACTION = "faction"

        @classmethod
        def from_esi_contact_type(cls, contact_type) -> "EsiContact.ContactType":
            """Create from an ESI contact type."""
            mapper = {
                "alliance": cls.ALLIANCE,
                "character": cls.CHARACTER,
                "corporation": cls.CORPORATION,
                "faction": cls.FACTION,
            }
            return mapper[contact_type]

    contact_id: int
    contact_type: ContactType
    standing: float
    label_ids: FrozenSet[int] = field(default_factory=frozenset)

    def __post_init__(self):
        object.__setattr__(self, "contact_id", int(self.contact_id))
        object.__setattr__(self, "contact_type", self.ContactType(self.contact_type))
        object.__setattr__(self, "standing", float(self.standing))
        object.__setattr__(self, "label_ids", frozenset(self.label_ids))

    def clone(self, **kwargs) -> "EsiContact":
        """Clone this object and optional overwrite field values with kwargs."""
        field_names = [field.name for field in fields(self.__class__)]
        params = {key: getattr(self, key) for key in field_names}
        params.update(kwargs)
        new_obj = self.__class__(**params)
        return new_obj

    def to_esi_dict(self) -> dict:
        """Return as a dict."""
        obj = {
            "contact_id": self.contact_id,
            "contact_type": self.ContactType(self.contact_type).value,
            "standing": self.standing,
        }
        if self.label_ids:
            obj["label_ids"] = sorted(list(self.label_ids))
        return obj

    @classmethod
    def from_esi_dict(cls, esi_dict: dict) -> "EsiContact":
        """Create new objects from an ESI contact."""
        return cls(
            contact_id=esi_dict["contact_id"],
            contact_type=EsiContact.ContactType.from_esi_contact_type(
                esi_dict["contact_type"]
            ),
            standing=esi_dict["standing"],
            label_ids=esi_dict.get("label_ids") or frozenset(),
        )

    @classmethod
    def from_eve_entity(
        cls, eve_entity: EveEntity, standing: float, label_ids=None
    ) -> "EsiContact":
        """Create new instance from an EveEntity object."""
        contact_type_map = {
            EveEntity.CATEGORY_ALLIANCE: cls.ContactType.ALLIANCE,
            EveEntity.CATEGORY_CHARACTER: cls.ContactType.CHARACTER,
            EveEntity.CATEGORY_CORPORATION: cls.ContactType.CORPORATION,
            EveEntity.CATEGORY_FACTION: cls.ContactType.FACTION,
        }
        if eve_entity.category not in contact_type_map:
            raise ValueError(
                f"{eve_entity}: Can not create from eve entity without category"
            )
        return cls(
            contact_id=eve_entity.id,
            contact_type=contact_type_map[eve_entity.category],
            standing=standing,
            label_ids=label_ids if label_ids else frozenset(),
        )

    @classmethod
    def from_eve_contact(cls, eve_contact: Any, label_ids=None) -> "EsiContact":
        """Create new instance from an EveContact object."""
        contact_type_map = {
            EveEntity.CATEGORY_ALLIANCE: cls.ContactType.ALLIANCE,
            EveEntity.CATEGORY_CHARACTER: cls.ContactType.CHARACTER,
            EveEntity.CATEGORY_CORPORATION: cls.ContactType.CORPORATION,
        }
        return cls(
            contact_id=eve_contact.eve_entity.id,
            contact_type=contact_type_map[eve_contact.eve_entity.category],
            standing=eve_contact.standing,
            label_ids=label_ids if label_ids else frozenset(),
        )


# pylint: disable = too-many-public-methods
@dataclass
class EsiContactsContainer:
    """Container of ESI contacts with their labels."""

    _contacts: Dict[int, EsiContact] = field(
        default_factory=dict, init=False, repr=False
    )
    _labels: Dict[int, EsiContactLabel] = field(
        default_factory=dict, init=False, repr=False
    )

    def add_label(self, label: EsiContactLabel):
        """Add contact label."""
        self._labels[label.id] = deepcopy(label)

    def add_contact(self, contact: EsiContact):
        """Add contact to container. Unknown label IDs will be removed."""
        if contact.label_ids:
            label_ids = {
                label_id for label_id in contact.label_ids if label_id in self._labels
            }
        else:
            label_ids = []
        self._contacts[contact.contact_id] = contact.clone(label_ids=label_ids)

    def add_eve_contacts(
        self, contacts: Iterable[object], label_ids: Optional[List[int]] = None
    ):
        """Add eve contacts to this container."""
        for contact in contacts:
            self.add_contact(EsiContact.from_eve_contact(contact, label_ids=label_ids))

    def remove_contact(self, contact: EsiContact):
        """Remove contact."""
        try:
            del self._contacts[contact.contact_id]
        except KeyError:
            raise ValueError(
                f"Unknown contact {contact} could not be removed."
            ) from None

    def remove_contacts(self, contacts: Iterable[EsiContact]):
        """Remove several contacts."""
        for contact in contacts:
            self.remove_contact(contact)

    def contact_by_id(self, contact_id: int) -> EsiContact:
        """Returns contact by it's ID.

        Raises ValueError when contact is not found.
        """
        try:
            return self._contacts[contact_id]
        except KeyError:
            raise ValueError(f"Contact with ID {contact_id} not found.") from None

    def contact_ids(self) -> Set[int]:
        """Return all contact IDs"""
        result = set(self._contacts)
        return result

    def contacts(self) -> Set[EsiContact]:
        """Fetch all contacts."""
        return set(self._contacts.values())

    def label_by_id(self, label_id) -> EsiContactLabel:
        """Returns label by it's ID.

        Raises ValueError when label is not found.
        """
        try:
            return self._labels[label_id]
        except KeyError:
            raise ValueError(f"Label with ID {label_id} not found.") from None

    def labels(self) -> Set[EsiContactLabel]:
        """Fetch all labels."""
        return set(self._labels.values())

    def war_target_label_id(self) -> Optional[int]:
        """Fetch the ID of the configured war target label."""
        for label in self._labels.values():
            if label.name.lower() == STANDINGSSYNC_WAR_TARGETS_LABEL_NAME.lower():
                return label.id
        return None

    def war_targets(self) -> Set[EsiContact]:
        """Fetch contacts that are war targets."""
        war_target_id = self.war_target_label_id()
        contacts = {obj for obj in self.contacts() if war_target_id in obj.label_ids}
        return contacts

    def remove_war_targets(self):
        """Remove war targets."""
        self.remove_contacts(self.war_targets())

    def clone(self) -> "EsiContactsContainer":
        """Return a clone of this object."""
        other = self.__class__.from_esi_contacts(
            contacts=self.contacts(), labels=self.labels()
        )
        return other

    # pylint: disable = protected-access
    def contacts_difference(
        self, other: "EsiContactsContainer"
    ) -> Tuple[Set[EsiContact], Set[EsiContact], Set[EsiContact]]:
        """Identify which contacts have been added, removed or changed."""
        current_contact_ids = set(self._contacts.keys())
        other_contact_ids = set(other._contacts.keys())
        removed = {
            contact
            for contact_id, contact in self._contacts.items()
            if contact_id in (current_contact_ids - other_contact_ids)
        }
        added = {
            contact
            for contact_id, contact in other._contacts.items()
            if contact_id in (other_contact_ids - current_contact_ids)
        }
        added_and_changed = set(other._contacts.values()) - set(self._contacts.values())
        changed = added_and_changed - added
        return added, removed, changed

    def contacts_to_esi_dicts(self) -> List[dict]:
        """Convert contacts into a stable dictionary."""
        return [
            obj.to_esi_dict()
            for obj in sorted(self._contacts.values(), key=lambda o: o.contact_id)
        ]

    def labels_to_esi_dicts(self) -> List[dict]:
        """Convert labels into a stable dictionary."""
        return [
            obj.to_esi_dict()
            for obj in sorted(self._labels.values(), key=lambda o: o.id)
        ]

    def to_dict(self) -> dict:
        """Convert this object into a stable dictionary."""
        data = {
            "contacts": self.contacts_to_esi_dicts(),
            "labels": self.labels_to_esi_dicts(),
        }
        return data

    def version_hash(self) -> str:
        """Calculate hash for current contacts & label in order to identify changes."""
        data = self.to_dict()
        return hashlib.md5(json.dumps(data).encode("utf-8")).hexdigest()

    @classmethod
    def from_esi_contacts(
        cls,
        contacts: Optional[Iterable[EsiContact]] = None,
        labels: Optional[Iterable[EsiContactLabel]] = None,
    ) -> "EsiContactsContainer":
        """Create new object from Esi contacts."""
        obj = cls()
        if labels:
            for label in labels:
                obj.add_label(label)
        if contacts:
            for contact in contacts:
                obj.add_contact(contact)
        return obj

    @classmethod
    def from_esi_dicts(
        cls,
        contacts: Optional[Iterable[dict]] = None,
        labels: Optional[Iterable[dict]] = None,
    ) -> "EsiContactsContainer":
        """Create new object from ESI contacts and labels."""
        obj = cls()
        if labels:
            for label in labels:
                obj.add_label(EsiContactLabel.from_esi_dict(label))
        if contacts:
            for contact in contacts:
                obj.add_contact(EsiContact.from_esi_dict(contact))
        return obj
