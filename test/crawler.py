import time
import requests
import pandas as pd

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class Stock:
    '''
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
        df = df.loc[(df['CFICode'] == 'ESVUFR') | (df['CFICode'] == 'EDSDDR') | (df['CFICode'] == 'CEOGEU') \
                    | (df['CFICode'] == 'CEOGDU') | (df['CFICode'] == 'CEOGMU') | (df['CFICode'] == 'CEOGCU') \
                    | (df['CFICode'] == 'CEOJEU') | (df['CFICode'] == 'CEOIBU') | (df['CFICode'] == 'CEOIEU') \
                    | (df['CFICode'] == 'CEOIRU') | (df['CFICode'] == 'CEOJLU') | (df['CFICode'] == 'CEOGBU') \
                    | (df['CFICode'] == 'CMXXXU') | (df['CFICode'] == 'CBCIXU')]
        print(df)
    '''

    '''
    def preprocessingStockList(self):
        # Read listed company list csv file and preprocess
        df = pd.read_csv('./data/Listed-Company-List.csv')
        df = df.drop(['股價日期', '成交', '漲跌價', '漲跌幅', '面值(元)', \
                      '股本(億)', '發行量(萬張)', '市值(億)', '成立年數', '股票期貨', \
                      '選擇權', '權證', '公司債', '私募股', '特別股', \
                      '董事長', '總經理'], axis=1)
        print(df)
    '''

    # Get stock list from twse.
    def getStockList(self):
        # Get listed company list (上市股票清單) from <https://isin.twse.com.tw/isin/C_public.jsp?strMode=2>
        headers = self.getHeaders()
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        res = requests.get(url, headers=headers)
        df = pd.read_html(res.text, encoding='big5hkscs')[0]
        df.columns = df.iloc[0]
        df = df.drop('備註', axis=1)
        df.columns = ['股票代號及名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']
        df1 = df.drop(df[(df.市場別!='上市')].index)
        df.loc[df['類型'].str.contains('RW'), '類型'] = '上市認購(售)權證'

        time.sleep(10)

        # Get OCT company list (上櫃股票清單) from <https://isin.twse.com.tw/isin/C_public.jsp?strMode=4>
        headers = self.getHeaders()
        url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
        res = requests.get(url, headers=headers)
        df = pd.read_html(res.text, encoding='big5hkscs')[0]
        df.columns = df.iloc[0]
        df = df.drop('備註', axis=1)
        df.columns = ['股票代號及名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']
        df2 = df.drop(df[(df.市場別)!='上櫃'].index)
        df.loc[df['類型'].str.contains('RW'), '類型'] = '上櫃認購(售)權證'

        # Merge df1 and df2 to one dataframe
        df = pd.concat([df1, df2])
        df['股票代號'] = df['股票代號及名稱'].map(lambda x:x.split('　')[0])
        df['股票名稱'] = df['股票代號及名稱'].map(lambda x:x.split('　')[-1])
        df = df[['股票代號', '股票名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']]
        df = df.set_index('股票代號')
        df.loc[df['類型'].str.contains('ES'), '類型'] = '股票'
        df.loc[df['類型'].str.contains('CMX'), '類型'] = 'ETN'
        df.loc[df['類型'].str.contains('CEO'), '類型'] = 'ETF'
        df.loc[df['類型'].str.contains('EDS'), '類型'] = '臺灣存託憑證(TDR)'
        df.loc[df['類型'].str.contains('CBC'), '類型'] = '受益證券-不動產投資信託'
        df.loc[df['類型'].str.contains('DA'), '類型'] = '受益證券-資產基礎證券'
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