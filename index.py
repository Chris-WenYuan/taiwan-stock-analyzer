from lib.taiwan_stock import TaiwanStock
from lib.mysql import MySQL

ts = TaiwanStock()
ms = MySQL()

# 使用 getStockList() 取得台灣上市上櫃股票清單，然後將清單儲存在 stockList.csv
stockList = ts.getStockList(filename='stockList.csv')

# 連接至本地端 MySQL 資料庫
ms.connectDB(host='localhost', user='chris', password='850806', database='stock')
ms.createStockListTable(stockList)