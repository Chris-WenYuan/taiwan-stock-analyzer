# lib 資料夾中各檔案使用方法

### `taiwan_stock.py` 使用方法

```python=
from lib.taiwan_stock import TaiwanStock # 引入 taiwan_stock.py

stock = TaiwanStock() # 建立物件

# 爬取台灣上市上櫃股票清單，並將結果以 pandas dataframe 形式回傳
# 此外，上市上櫃股票清單會以檔名 stockList.csv 儲存在當前目錄下
df = stock.getStockList(filename='stockList.csv')
```

### `mysql.py` 使用方法

```python=
from lib.mysql import MySQL # 引入 mysql.py

mysql = MySQL() # 建立物件

# 連接至 MySQL 並回傳資料庫物件
# host, user, password, database 參數請根據自己的設定去配置
db = mysql.connectDB(host='localhost', user='chris', password='850806', database='stock')

# 將台灣上市櫃股票清單存入 MySQL 資料庫的 stockList table 中
# df 為 getStockList() 所回傳的 pandas dataframe
mysql.createStockListTable(df)
```