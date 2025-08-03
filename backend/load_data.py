import pandas as pd

def get_data():
    return pd.read_csv("Data/brent_processed.csv", parse_dates=['Date'])
