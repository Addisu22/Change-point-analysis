import pandas as pd

def compute_volatility(df):
    df = df.copy()
    df['Volatility'] = df['LogReturn'].rolling(window=30).std()
    return df[['Date', 'Volatility']].dropna()

def event_impacts(df):
    # Dummy logic for events. Replace with real event mapping.
    events = {
        '2022-03-01': 'Russia-Ukraine Conflict',
        '2020-04-01': 'COVID-19 Lockdown',
    }
    df['Event'] = df['Date'].astype(str).map(events).fillna('')
    df['Impact'] = df['LogReturn'].where(df['Event'] != '', 0)
    return df[df['Event'] != ''][['Date', 'Event', 'Impact']]
