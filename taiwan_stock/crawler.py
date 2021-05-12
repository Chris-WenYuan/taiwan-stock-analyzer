import os
import json
import requests

from tqdm import tqdm
from re import findall
from time import sleep
from curses import wrapper
from bs4 import BeautifulSoup
from pandas_datareader import data
from fake_useragent import UserAgent
from requests_html import HTMLSession
from datetime import datetime, date, timedelta
from pandas import read_html, concat, DataFrame, set_option

set_option('display.unicode.ambiguous_as_wide', True)
set_option('display.unicode.east_asian_width', True)

"""Crawl taiwan stock list"""
def getStockList():
    print('[crawler.getStockList] 正在抓取台灣上市上櫃股票清單......')

    # Crawl taiwan listed company list from <https://isin.twse.com.tw/isin/C_public.jsp?strMode=2>
    headers = _getHeaders()
    url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    res = requests.get(url, headers=headers)
    df1 = read_html(res.text, encoding='utf8')[0]
    df1.columns = df1.iloc[0]
    df1 = df1.drop('備註', axis=1)
    df1.columns = ['股票代號及名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']
    df1 = df1.drop(df1[(df1.市場別!='上市')].index)
    df1.loc[df1['類型'].str.contains('RW'), '類型'] = '上市認購(售)權證'

    sleep(3)

    # Crawl taiwan OCT company list from <https://isin.twse.com.tw/isin/C_public.jsp?strMode=4>
    headers = _getHeaders()
    url = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
    res = requests.get(url, headers=headers)
    df2 = read_html(res.text, encoding='utf8')[0]
    df2.columns = df2.iloc[0]
    df2 = df2.drop('備註', axis=1)
    df2.columns = ['股票代號及名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']
    df2 = df2.drop(df2[(df2.市場別)!='上櫃'].index)
    df2.loc[df2['類型'].str.contains('RW'), '類型'] = '上櫃認購(售)權證'

    # Merge listed company list (df1) and OCT company list (df2)
    df = concat([df1, df2])
    df['股票代號'] = df['股票代號及名稱'].map(lambda x:x.split()[0])
    df['股票名稱'] = df['股票代號及名稱'].map(lambda x:x.split()[-1])
    df = df[['股票代號', '股票名稱', 'ISIN Code', '上市日', '市場別', '產業別', '類型']]
    df.reset_index(inplace=True, drop=True)
    df.loc[df['類型'].str.contains('ES'), '類型'] = '股票'
    df.loc[df['類型'].str.contains('CMX'), '類型'] = 'ETN'
    df.loc[df['類型'].str.contains('CEO'), '類型'] = 'ETF'
    df.loc[df['類型'].str.contains('EDS'), '類型'] = '臺灣存託憑證(TDR)'
    df.loc[df['類型'].str.contains('CBC'), '類型'] = '受益證券-不動產投資信託'
    df.loc[df['類型'].str.contains('DA'), '類型'] = '受益證券-資產基礎證券'
    df.loc[df['類型'].str.contains('EP'), '類型'] = '特別股'
    df = df.set_index('股票代號')

    df = df[(df.類型!='上市認購(售)權證')&(df.類型!='上櫃認購(售)權證')] # Remove the rows by 類型=('上市認購(售)權證' or '上櫃認購(售)權證')
    df = df.sort_index() # Sort by 股票代號

    filename = 'stockList.csv'
    base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', '股票列表')
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    file_path = os.path.join(base_path, filename)
    df.to_csv(file_path)

    print('[crawler.getStockList] 上市櫃股票股票清單儲存至 <./output/股票列表/stockList.csv>')
    print('[crawler.getStockList] 完成\n')
    return df

"""Get taiwan stock histories by specific markets and types"""
def getAllStockHistories(markets, types):
    df = getStockList()

    print('[crawler.getAllStockHistories] 正在抓取全部個股的歷史紀錄......')
    print('[crawler.getAllStockHistories] 市場別(markets):', markets)
    print('[crawler.getAllStockHistories] 類型(types):', types)

    result_df = df[(df['市場別'].isin(markets))&(df['類型'].isin(types))]

    pbar = tqdm(total=len(result_df), desc='[crawler.getAllStockHistories]')
    for sid, row in result_df.iterrows():
        try:
            if row['市場別'] == '上市':
                market = '.TW'
            elif row['市場別'] == '上櫃':
                market = '.TWO'
            history_df = data.get_data_yahoo(sid+market, '2000-01-01', date.today().strftime('%Y-%m-%d'))
            
            if row['類型'] == '股票':
                base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', '歷史股價', row['市場別'], row['類型'], row['產業別'])
            else:
                base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', '歷史股價', row['市場別'], row['類型'])
            filename = '{}.csv'.format(sid)
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            file_path = os.path.join(base_path, filename)
            history_df.to_csv(file_path)
        except Exception as e:
            pass
        sleep(0.1)
        pbar.update(1)
    pbar.close()

    print('[crawler.getAllStockHistories] 個股歷史紀錄儲存至 <./output/歷史紀錄/>')
    print('[crawler.getAllStockHistories] 完成\n')

"""Get stock real time price by given sid"""
def getRealTime(sid):
    wrapper(_getRealTime, sid)

"""Get financial news"""
def getNews(start_date, end_date):
    NEWS_CATEGORY_API = 'https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={}&endAt={}&limit=30'
    NEWS_CONTENT_URL = 'https://news.cnyes.com/news/id/{}?exp=a'
    base_path = os.path.join(os.path.abspath(os.getcwd()), 'output', 'news')
    filename = '{}_{}.txt'.format(start_date, end_date)

    current_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    if not os.path.exists(base_path):
        os.makedirs(base_path)

    print('[crawler.getNews] 準備抓取台股相關新聞，並儲存至 {}'.format(base_path))
    while current_date <= end_date:
        current_date_second = int(current_date.timestamp())
        url = NEWS_CATEGORY_API.format(current_date_second, current_date_second)
        filename = current_date.strftime('%Y-%m-%d.txt')

        file_path = os.path.join(base_path, filename)
        f = open(file_path, 'w')
        
        print('[crawler.getNews] 抓取 {} 的新聞'.format(str(current_date).replace(' 00:00:00', '')))
        session = HTMLSession()
        response = session.get(url).json()
        posts = response['items']['data']
        pbar = tqdm(total=len(posts), desc='[crawler.getNews]')
        for post in posts:
            try:
                postSession = HTMLSession()
                article_url = NEWS_CONTENT_URL.format(post['newsId'])
                title = post['title'].replace('\n', '')
                f.write('[文章標題]: {}\n'.format(title))
                postResponse = postSession.get(article_url)
                postResponse.html.render(sleep=0.1, timeout=30)
                article = postResponse.html.find('div[itemprop="articleBody"]')[0].text.replace('\n', '')
                f.write('[文章內容]: {}\n'.format(article))
                try:
                    relation = postResponse.html.find('section[class="_3EMg"]')[0].text.replace('\n', '').replace('相關個股', '')
                    stocks = findall(u'[\u4e00-\u9fa5]+[-]?[A-Z]*', relation)
                    f.write('[相關個股]: {}\n'.format(','.join(stocks)))
                    f.write('--------------------\n')
                except:
                    f.write('[相關個股]: \n')
                    f.write('--------------------\n')
            except Exception as e:
                pass
            pbar.update(1)
        f.close()
        pbar.close()

        current_date += timedelta(days=1)
    print('[crawler.getNews] 完成\n')

"""Get three institutional investors information"""
def getInstitutionalInvestors():
    TWSE_URL = 'http://www.twse.com.tw/fund/T86?response=json&date={}&selectType=ALL' # ex: 20120502
    TPEX_URL = 'http://www.tpex.org.tw/web/stock/3insti/daily_trade/3itrade_hedge_result.php?l=zh-tw&se=AL&t=D&d={}' # ex: 106/02/06

    # Get listed company three institutional investors information
    headers = _getHeaders()
    url = TWSE_URL.format('20210429')
    res = requests.get(url, headers=headers)
    res = json.loads(res.text)
    res = dict((k, res[k]) for k in ('fields','data') if k in res) # Get sub-dict from res with keys=['fields', 'data']
    df = DataFrame(res['data'], columns=res['fields'])
    print(df)

    # Get OCT three institutional investors information
    headers = _getHeaders()
    url = TPEX_URL.format('110/05/03')
    res = requests.get(url, headers=headers)
    res = json.loads(res.text)
    res = dict((k, res[k]) for k in ('reportTitle', 'aaData') if k in res) # Get sub-dict from res with keys=['aaData']
    columns = ['證券代號', '證券名稱', '外陸資買進股數(不含外資自營商)', '外陸資賣出股數(不含外資自營商)', '外陸資買賣超股數(不含外資自營商)', \
               '外資自營商買進股數', '外資自營商賣出股數', '外資自營商買賣超股數', '外陸資買進股數', '外陸資賣出股數', '外陸資買賣超股數', \
               '投信買進股數', '投信賣出股數', '投信買賣超股數', '自營商買進股數(自行買賣)', '自營商賣出股數(自行買賣)', '自營商買賣超股數(自行買賣)', \
               '自營商買進股數(避險)', '自營商賣出股數(避險)', '自營商買賣超股數(避險)', '自營商買進股數', '自營商賣出股數', '自營商買賣超股數', \
               '三大法人買賣超股數合計', 'unknown']
    df = DataFrame(res['aaData'], columns=columns)
    print(df)

"""Get fake web headers"""
def _getHeaders():
    ua = UserAgent()
    user_agent = ua.random
    headers = {'user-agent': user_agent}
    return headers

"""Call by getRealTime function"""
def _getRealTime(stdscr, sid):
    stdscr.clear() # Clear screen
    stdscr.addstr(0, 0, '[crawler.getRealTime] 取得選定之個股的當前股價：')

    while True:
        result = []
        for i in range(len(sid)):
            response = requests.get('https://tw.stock.yahoo.com/q/q?s=' + sid[i])
            soup = BeautifulSoup(response.text.replace('加到投資組合', ''), 'lxml')
            stock_date = soup.find('font', {'class', 'tt'}).getText().strip()[-9:]
            tables = soup.find_all('table')[2]
            tds = tables.find_all('td')[0:11]
            result.append((stock_date,) + tuple(td.getText().strip() for td in tds))

        df = DataFrame(result, columns=['日期', '股票代號', '時間', '成交', '買進', '賣出', '漲跌', '張數', '昨收', '開盤', '最高', '最低'])
        rows = df.to_string().split('\n')

        for i in range(len(rows)):
            stdscr.addstr(i+1, 0, rows[i])

        stdscr.refresh()
        sleep(0.5)
    stdscr.getkey()
