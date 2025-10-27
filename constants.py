"""
Centralized constants for the BUCC Discord Bot.

This module contains all channel names, role names, and mapping dictionaries
used throughout the bot to avoid magic strings and code duplication.
"""

from typing import Final


class ChannelNames:
    """Discord channel names used by the bot."""

    VERIFICATION: Final[str] = "automatic-verification"
    NOTIFICATION: Final[str] = "notification"
    MESSAGE_FORWARD: Final[str] = "message-forward-by-bot"
    TEST_COMMAND: Final[str] = "test-com"
    GENERAL: Final[str] = "general"


class ButtonIDs:
    """Discord UI component custom IDs."""

    VERIFY_ME: Final[str] = "verify_me_button"


class RoleNames:
    """Discord role names required in each server."""

    GOVERNING_BODY: Final[str] = "Governing Body"
    EXECUTIVE_BODY: Final[str] = "Executive Body"
    SENIOR_EXECUTIVE: Final[str] = "Senior Executive"
    ALUMNI: Final[str] = "Alumni"
    FACULTY: Final[str] = "Faculty"

    # Department roles
    COMMUNICATION_MARKETING: Final[str] = "C&M"
    CREATIVE: Final[str] = "Creative"
    EVENT: Final[str] = "Event"
    FINANCE: Final[str] = "Finance"
    HR: Final[str] = "HR"
    PRESS_RELEASE: Final[str] = "Press Release"
    RND: Final[str] = "R&D"


# All required roles for server setup
REQUIRED_ROLES: Final[list[str]] = [
    RoleNames.GOVERNING_BODY,
    RoleNames.EXECUTIVE_BODY,
    RoleNames.SENIOR_EXECUTIVE,
    RoleNames.ALUMNI,
    RoleNames.FACULTY,
    RoleNames.COMMUNICATION_MARKETING,
    RoleNames.CREATIVE,
    RoleNames.EVENT,
    RoleNames.FINANCE,
    RoleNames.HR,
    RoleNames.PRESS_RELEASE,
    RoleNames.RND,
]

# All required channels for server setup
REQUIRED_CHANNELS: Final[list[str]] = [
    ChannelNames.VERIFICATION,
    ChannelNames.NOTIFICATION,
    ChannelNames.MESSAGE_FORWARD,
]


class DesignationMappings:
    """Maps full designation names to their abbreviations."""

    MAPPING: Final[dict[str, str]] = {
        "Senior Executive": "SE",
        "Executive": "Executive",
        "General Member": "GM",
        "Governing Body": "GB",
        "Executive Body": "EB",
        "Alumni": "Alumni",
        "Faculty": "Faculty",
    }


class DepartmentMappings:
    """Maps full department names to their abbreviations."""

    MAPPING: Final[dict[str, str]] = {
        "Communication and Marketing": "C&M",
        "Creative": "Creative",
        "Event Management": "EM",
        "Finance": "Finance",
        "Human Resources": "HR",
        "Press Release and Publications": "PR",
        "Research and Development": "R&D",
    }


# Special designations that don't require department roles
LEADERSHIP_DESIGNATIONS: Final[set[str]] = {
    "Governing Body",
    "Executive Body",
    "Alumni",
}
