import pandas as pd

def gSheet():
    sheet_id = '1LFKjRZ6l-prXz-QFxSZtT-FPTtzEIfTKMyuddyK5NE4'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv'
    df = pd.read_csv(url)
    
    # Create a dictionary from the dataframe
    data_dict = df.set_index(df.columns[0]).T.to_dict('list')
    
    return data_dict