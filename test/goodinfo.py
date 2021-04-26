import requests
import pandas as pd
import time

from fake_useragent import UserAgent
from bs4 import BeautifulSoup

ua = UserAgent()
user_agent = ua.random
time_interval = 15

headers = {'user-agent': user_agent}

url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID=2330"

count = 0
while True:
    try:
        count += 1
        res = requests.get(url, headers=headers)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html.parser')
        data = soup.find(id='txtFinDetailData')
        dfs = pd.read_html(data.prettify())
        df = dfs[0]
        df.columns = df.columns.get_level_values(3)
        print(df)
        print(count)
    except:
        print(soup)

    time.sleep(time_interval)
