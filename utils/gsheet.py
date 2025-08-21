import pandas as pd
import config
import logging

logger = logging.getLogger(__name__)


def gSheet() -> dict:
    """
    Fetches data from a Google Sheet and returns it as a dictionary.

    The Google Sheet ID is retrieved from the configuration.
    The first column of the sheet is used as keys, and subsequent columns as values in a list.

    Returns:
        A dictionary where keys are from the first column and values are lists
        of data from the rest of the columns.
    """
    try:
        url = f"https://docs.google.com/spreadsheets/d/{config.GOOGLE_SHEET_ID}/export?format=csv"
        df = pd.read_csv(url)

        # Create a dictionary from the dataframe
        # The first column is used as the index (keys), and rows are converted to lists (values)
        data_dict = df.set_index(df.columns[0]).T.to_dict("list")

        logger.info("Successfully fetched data from Google Sheet.")
        return data_dict
    except Exception as e:
        logger.error(f"Error fetching data from Google Sheet: {e}")
        return {}
