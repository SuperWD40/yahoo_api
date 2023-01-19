import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime 
from datetime import datetime, date, timedelta
import os 

def get_history(ticker, period, continuous = False):
        # Send request to the web site
        period1, period2, delta = timeperiod(period)
        url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval=1d&events=history&includeAdjustedClose=true'
        response = requests.get(
            url,
            headers={'User-Agent': 'Safari/537.36'},
            timeout= 10
        )
        
        # Donwload, read as DataFrame and delete history.csv 
        with open(f'{ticker}.csv', 'w') as f:
                f.write(response.text)

        df = pd.read_csv(f'{ticker}.csv')
        os.remove(f'{ticker}.csv')
        
        # Clean DataFrame
        df = df.set_index('Date')
        df.index = pd.to_datetime(df.index)
        df = df.drop('Close',axis=1)
        df = df.rename(columns={'Adj Close':'Close'})
        df = df.apply(pd.to_numeric, errors='coerce')
        df['Volume'].fillna(0, inplace=True)
        df.dropna(subset=['Open'], inplace=True)
        
        # If asked transform history into continuous one
        if continuous != False: df = df.resample('D').ffill()[-delta:]
        return(df)
    
def timeperiod(period):
    # Transform string into timestamp
    timeDict = {
            'max': 0,
            '10y': 3650,
            '5y': 1825,
            '1y': 365,
            '6m': 182,
            '1m': 30,
            '5d': 5,
            '1d': 1
        }
    delta = timeDict[period]
    if delta == 0:
        period1 = 0
    else:
        period1 = datetime.now() - timedelta(days=delta)
        period1 = str(int(period1.timestamp()))
    period2 = str(int(datetime.now().timestamp()))
    return(period1, period2, delta)
