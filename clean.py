import os, pandas as pd
RAW = os.path.join('data','raw','owid-covid-data.csv')
OUT = os.path.join('data','processed','covid_clean.csv')

def clean(df):
    cols = ['iso_code','location','date','total_cases','new_cases','total_deaths','new_deaths','people_vaccinated','people_fully_vaccinated','population']
    keep = [c for c in cols if c in df.columns]
    df = df[keep].copy()
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    df.to_csv(OUT, index=False)
    print('Saved cleaned file to', OUT)

if __name__ == '__main__':
    if os.path.exists(RAW):
        df = pd.read_csv(RAW, parse_dates=['date'])
        clean(df)
    else:
        alt = os.path.join('data','raw','owid-covid-data.csv')
        if os.path.exists(alt):
            print('Raw not found, using sample.')
            df = pd.read_csv(alt, parse_dates=['date'])
            clean(df)
        else:
            print('No raw data found. Please place owid-covid-data.csv into data/raw/')
