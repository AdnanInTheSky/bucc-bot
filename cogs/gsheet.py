import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

def gSheet():
    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
    df = pd.read_csv(url)
    
    # Create a dictionary from the dataframe
    data_dict = df.set_index(df.columns[0]).T.to_dict('list')
    
    return data_dict

print(gSheet())