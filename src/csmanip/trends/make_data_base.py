import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def make_database(data, file_name):
    start_date = pd.to_datetime(data[0][0])
    end_date = pd.to_datetime(data[-1][0])
    
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    data_base = []
    data_index = 0

    for date in date_range:
        found = False
        
        while data_index < len(data):
            record_date = pd.to_datetime(data[data_index][0])
            
            if record_date == date:
                data_base.append([
                    date.year, date.month, date.day,
                    data[data_index][1],
                    data[data_index][2],
                    data[data_index][3]
                ])
                data_index += 1
                found = True
                break
            
            data_index += 1

        if not found:
            data_base.append([date.year, date.month, date.day, -99, -99, -99])
    
    df = pd.DataFrame(data_base, columns=['Year', 'Month', 'Day', 'V1', 'V2', 'V3'])
    df.to_excel(file_name, index=False)

    return df


def clean_missing_data(df):
    return df[(df[['V', 'V2', 'V3']] != -99).all(axis=1)]


def normalize_data(df):
    normalized_df = df.copy()
    
    for col in ['V1', 'V2', 'V3']:
        if df[col].min() != df[col].max():
            normalized_df[col] = ((df[col] - df[col].min()) / (df[col].max() - df[col].min())) * 0.6 + 0.2
    
    return normalized_df

