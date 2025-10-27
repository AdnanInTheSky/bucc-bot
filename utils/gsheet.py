"""
Google Sheets data fetching utilities.

This module provides functions to fetch and parse member data from
Google Sheets published to the web as CSV.
"""

import pandas as pd
import logging

import config

logger = logging.getLogger(__name__)


class SheetFetchError(Exception):
    """Raised when fetching data from Google Sheet fails."""

    pass


def fetch_member_data_from_sheet() -> dict[str, list[str]]:
    """
    Fetch member data from the configured Google Sheet.

    The sheet must be published to web with CSV export enabled.
    First column (Discord username) becomes dict keys, remaining
    columns become list values [name, department, designation].

    Returns:
        Dictionary mapping Discord usernames to member data lists

    Raises:
        SheetFetchError: If sheet cannot be accessed or parsed
    """
    try:
        sheet_url = f"https://docs.google.com/spreadsheets/d/{config.GOOGLE_SHEET_ID}/export?format=csv"
        dataframe = pd.read_csv(sheet_url)

        member_data = dataframe.set_index(dataframe.columns[0]).T.to_dict("list")

        logger.info("Successfully fetched member data from Google Sheet")
        return member_data

    except pd.errors.EmptyDataError:
        logger.error("Google Sheet is empty")
        raise SheetFetchError("Google Sheet contains no data")

    except pd.errors.ParserError as e:
        logger.error(f"Failed to parse Google Sheet CSV: {e}")
        raise SheetFetchError(f"Invalid CSV format: {e}")

    except Exception as e:
        logger.error(f"Unexpected error fetching Google Sheet: {e}")
        raise SheetFetchError(f"Failed to fetch sheet data: {e}")
