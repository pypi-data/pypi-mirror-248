"""Settings for standingssync."""

from app_utils.app_settings import clean_setting

STANDINGSSYNC_ADD_WAR_TARGETS = clean_setting("STANDINGSSYNC_ADD_WAR_TARGETS", False)
"""When enabled will automatically add or set war targets
 with standing = -10 to synced characters.
"""

STANDINGSSYNC_CHAR_MIN_STANDING = clean_setting(
    "STANDINGSSYNC_CHAR_MIN_STANDING", default_value=0.1, min_value=-10, max_value=10
)
"""Minimum standing a character needs to have in order to get alliance contacts.
Any char with a standing smaller than this value will be rejected.
Set to `0.0` if you want to allow neutral alts to sync.
"""

STANDINGSSYNC_STORE_ESI_CONTACTS_ENABLED = clean_setting(
    "STANDINGSSYNC_STORE_ESI_CONTACTS_ENABLED", False
)
"""Wether to store contacts received from ESI to disk. This is for debugging."""

STANDINGSSYNC_REPLACE_CONTACTS = clean_setting("STANDINGSSYNC_REPLACE_CONTACTS", True)
"""When enabled will replace contacts of synced characters with alliance contacts."""

STANDINGSSYNC_SYNC_TIMEOUT = clean_setting("STANDINGSSYNC_SYNC_TIMEOUT", 180)  # 3 hours
"""Duration in minutes after which a delayed sync for managers and characters
is reported as down. This value should be aligned with the frequency of the sync task.
"""

STANDINGSSYNC_UNFINISHED_WARS_EXCEPTION_IDS = clean_setting(
    "STANDINGSSYNC_UNFINISHED_WARS_EXCEPTION_IDS",
    [
        693125,
        716071,
        716072,
        716073,
        716864,
        717695,
        718307,
        718387,
        718575,
        718576,
        718619,
        718637,
        718638,
        718639,
        718640,
        718941,
        719186,
        719187,
        719188,
        719189,
        719226,
        719331,
        719336,
        719337,
        719423,
        719745,
        719751,
        719854,
        719890,
    ],
)
"""IDs of unfinished wars, with IDs below the above minimum threshold.
These wars will also be included in the list of unfinished wars,
despite there ID being below the minimum ID.

:private:
"""

STANDINGSSYNC_UNFINISHED_WARS_MINIMUM_ID = clean_setting(
    "STANDINGSSYNC_UNFINISHED_WARS_MINIMUM_ID", 719979
)
"""Smallest war ID to fetch from ESI.

All wars with smaller IDs are known to be already finished.
This is an optimization to avoid having to fetch >700K wars from ESI.

:private:
"""

STANDINGSSYNC_WAR_TARGETS_LABEL_NAME = clean_setting(
    "STANDINGSSYNC_WAR_TARGETS_LABEL_NAME", "WAR TARGETS"
)
"""Name of EVE contact label for war targets.
Needs to be created by the user for each synced character. Required to ensure that
war targets are deleted once they become invalid. Not case sensitive.
"""
