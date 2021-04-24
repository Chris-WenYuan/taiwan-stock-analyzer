import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Stock:
    # Get stock list from twse and tpex.
    def getStockList(self):
        headers = self.getHeaders()
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        res = requests.get(url, headers=headers)
        df = pd.read_html(res.text, encoding='big5hkscs')[0]
        df.columns = df.iloc[0]
        df = df.iloc[1:]
        df = df.drop('備註', axis=1)
        df = df.set_index('有價證券代號及名稱')
        df = df.loc[(df['CFICode'] == 'ESVUFR') | (df['CFICode'] == 'EDSDDR') | (df['CFICode'] == 'CEOGEU') | (df['CFICode'] == 'CEOGDU') | (df['CFICode'] == 'CEOGMU') | (df['CFICode'] == 'CEOGCU') | (df['CFICode'] == 'CEOJEU') | (df['CFICode'] == 'CEOIBU') | (df['CFICode'] == 'CEOIEU') | (df['CFICode'] == 'CEOIRU') | (df['CFICode'] == 'CEOJLU') | (df['CFICode'] == 'CEOGBU') | (df['CFICode'] == 'CMXXXU') | (df['CFICode'] == 'CBCIXU')]
        print(df)

    def getStockHistory(self):
        for year in range(2021, 2022):
            for month in range(1, 13):
                try:
                    headers = self.getHeaders()
                    date = "{:d}{:02d}01".format(year, month)
                    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=html&date=' + date + '&stockNo=2330'
                    #res = requests.get(url, headers=headers)
                    #soup = BeautifulSoup(res.text, 'html.parser')
                    #print(soup.find_all('table'))
                    dfs = pd.read_html(url)
                    print(dfs)

                    time.sleep(10)
                except:
                    print('FAIL: <' + url + '> does not exist.')
    
    def getHeaders(self):
        ua = UserAgent()
        user_agent = ua.random
        headers = {'user-agent': user_agent}
        
        return headers

stock = Stock()
stock.getStockList()