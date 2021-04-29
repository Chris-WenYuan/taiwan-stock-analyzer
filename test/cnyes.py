import requests
import time
import json
from datetime import datetime
from lxml import etree
import csv

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
    }
    
#將資料儲存成CSV檔案
def savefile(beginday,stopday,news):
    filename='cnyes-'+beginday+'~'+stopday+'.csv'
    with open(filename, 'a', newline='',encoding='utf8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(news)

#分析網頁資訊
def parse(headers,newsID,k,total,beginday,stopday):    
    fnews_url = 'https://news.cnyes.com/news/id/{}?exp=a'.format(newsID) #原始新聞網址    
    response = requests.get(fnews_url, headers)
    html=etree.HTML(response.content)   
    try: 
        title=html.xpath('//*[@id="content"]/div/div/div[2]/main/div[2]/h1/text()')[0] #新聞標題
        print('第 {} / {} 篇新聞: '.format(k,total),title)     
        posttime=html.xpath('//*[@id="content"]/div/div/div[2]/main/div[2]/div[2]/time/text()')[0] 
        posttime=posttime.split(' ')
        date=posttime[0]#新聞發佈日期
        time=posttime[1]#新聞發佈時間
        content=html.xpath('//*[@id="content"]/div/div/div[2]/main/div[3]/article/section/div[1]//text()')
        content=''.join(content).strip() #新聞內文
        content=content.replace('\n','')
        url=fnews_url.replace('?exp=a','')#原始新聞來源網址
        tag=html.xpath('//*[@id="content"]/div/div/div[2]/main/div[3]/article/section/nav[2]/a//text()')
        tag=','.join(tag).strip() #Tag
        news=[date,time,title,tag,content,url]
        # print("news:",news)
        
        #將資訊儲存成檔案(或寫入資料庫)
        savefile(beginday,stopday,news)
        
    except IndexError as IE:
        print('抓值範圍錯誤')
        print('html:' ,response.text)
        news={"title":None,"date":None,"content":None,"url":None,"tag":None }
    except OSError as OSErr:
        print('OSError:{}'.format(OSErr))
    except requests.exceptions.ConnectionError as REC:
        print('連線錯誤')
    except urllib3.exceptions.ProtocolError as UEP:
        print('連線錯誤')
    return news

#分析文章數量
def crawler(beginday,stopday):   
    #搜尋新聞開始日,格式為 'Y-M-D'
    be_day=beginday
    #搜尋新聞結束日
    st_day=stopday
    #日期格式轉換成時間戳型式
    startday = int(datetime.timestamp(datetime.strptime(be_day, "%Y-%m-%d")))
    endday = int(datetime.timestamp(datetime.strptime(st_day, "%Y-%m-%d"))-1)
    url ='https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={}&endAt={}&limit=30'.format(startday,endday)
    res = requests.get(url, headers)

    newsID_lt=[]
    #獲取搜尋總頁數
    last_page = json.loads(res.text)['items']['last_page']
    print('總共 {} 頁'.format(last_page))
    # 篩選 newsId 值
    newsIDlist=json.loads(res.text)['items']['data']

    #獲取第一頁各個新聞的 newsId
    for i in newsIDlist:
        newsID=i['newsId']
        newsID_lt.append(newsID)
    print('正在獲取第 1 頁 newsId')
    time.sleep(1)

    #進行翻頁並獲取各頁面的 newsId
    for p in range(2,last_page+1):
        oth_url ='https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={}&endAt={}&limit=30&page={}'.format(startday,endday,p)
        res=requests.get(oth_url, headers)
        print('正在獲取第 {} 頁 newsId'.format(p))
        # 獲取新聞的newsId
        newsIDlist=json.loads(res.text)['items']['data']
        for j in newsIDlist:        
            newsID=j['newsId']
            newsID_lt.append(newsID)
        #抓取每頁newsId的延遲時間
        time.sleep(1)
    
    # 由 newsId 獲取詳細新聞內容
    for k,n in enumerate(newsID_lt):    
        data=parse(headers,n,k+1,len(newsID_lt),beginday,stopday)
        #抓取每篇完整新聞的延遲時間
        time.sleep(0.5)

def main(beginyear,beginmonth,crawlrange,stopmonth=12):
    #確認抓上半月或下半月
    if crawlrange==1:
        #抓上半個月
        for m in range(beginmonth,stopmonth+1):        
            if m < 10:
                beginday='{}-0{}-01'.format(beginyear,m)
                stopday='{}-0{}-16'.format(beginyear,m)
            else:
                beginday='{}-{}-01'.format(beginyear,m)
                stopday='{}-{}-16'.format(beginyear,m)
            crawler(beginday,stopday)
            if m ==12:
                print('程式執行完成')
                break
            # else:
                # print('切換到 {} 月份等待5秒'.format(m+1))
            time.sleep(5)

    elif crawlrange==2:
        #抓下半個月
        for m in range(beginmonth,stopmonth+1):
            beginday='{}-0{}-16'.format(beginyear,m)  
            if m == 9:        
                stopday='{}-{}-01'.format(beginyear,m+1)
            elif m >= 10:
                beginday='{}-{}-16'.format(beginyear,m)
                if m == 12:
                    stopday='{}-01-01'.format(beginyear+1)
                else:
                    stopday='{}-{}-01'.format(beginyear,m+1)
            else:
                stopday='{}-0{}-01'.format(beginyear,m+1)
            
            crawler(beginday,stopday)
            if m ==stopmonth:
                print('程式執行完成')
                break
            # else:
                # print('切換到 {} 月份等待5秒'.format(m+1))
            time.sleep(5)
    else:
        print('爬取區間設定錯誤!')

if __name__ == '__main__':
    beginyear=2021  #爬取新聞年份
    beginmonth=4    #爬取新聞開始月份
    stopmonth=4    #爬取停止月份
    
    #爬取月份區間,因為測試直接抓一整個月伺服器回傳的資訊可能會出現異常,
    #所以分成上半月(1~15日)和下半月(16~月底)
    for i in range(1,3):    #先爬上半月再爬下半月
        main(beginyear,beginmonth,i,stopmonth) 