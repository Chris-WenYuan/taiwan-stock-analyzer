from lib.taiwan_stock import TaiwanStock
from lib.mysql import MySQL

if __name__ == '__main__':
    stock = TaiwanStock()
    mysql = MySQL()

    '''
    # 使用 getStockList() 取得台灣上市上櫃股票清單，然後將清單儲存在 stockList.csv
    df_stockList = stock.getStockList(filename='stockList.csv')
    # print(df_stockList)
    '''

    # 連接至本地端 MySQL 資料庫(host, user, password, database 參數請依照你的資料庫設定做更改)
    db = mysql.connectDB(host='localhost', user='chris', password='850806', database='stock')

    '''
    # 將 getStockList() 回傳的股票清單存入 MySQL 資料庫的 table 中
    mysql.createStockListTable(stockList)
    '''

    # 查詢類型為股票且市場別為上市的股票
    sql = 'SELECT * FROM stockList WHERE 類型="股票" AND 市場別="上市" ORDER BY 股票代號 ASC;'
    df_result = mysql.queryDB(db, sql=sql)
    # print(df_result)

    # 從台灣證券交易所的網站爬取個股歷史資料
    stock.crawlStockHistoryFromTwse(df_result)
