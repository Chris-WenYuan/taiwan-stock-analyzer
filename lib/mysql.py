import pymysql

from sqlalchemy import create_engine
from pandas import DataFrame

class MySQL:
    def __init__(self):
        self.db = 0
        self.engine = 0
        self.database = 0 # 你將用來存股票資料的 MySQL 資料庫名稱
    
    def connectDB(self, host='localhost', user='chris', password='850806', database='stock'):
        self.database = database
        self.db = pymysql.connect(host=host, user=user, password=password,database=self.database)
        print('[INFO] 已連接至 {} 資料庫。'.format(self.database))
        
        connection_string = 'mysql+pymysql://{}:{}@{}:3306/{}'.format(user, password, host, self.database)
        self.engine = create_engine(connection_string)
        print('[INFO] 連線引擎 <{}> 建立成功。'.format(connection_string))

        return self.db
    
    def createStockListTable(self, df):
        cur = None
        if self.db is not None:
            cur = self.db.cursor()
        if cur is not None:
            # 如果 stockList table 存在，就先刪除
            sql = 'DROP TABLE IF EXISTS `stockList`;'
            cur.execute(sql)
            self.db.commit()

            # 建立 stockList table
            sql = 'CREATE TABLE `stockList`( \
                `股票代號` VARCHAR(20) NOT NULL, \
                `股票名稱` VARCHAR(20), \
                `ISIN Code` CHAR(12), \
                `上市日` CHAR(10), \
                `市場別` CHAR(2), \
                `產業別` VARCHAR(20), \
                `類型` VARCHAR(20) \
            )ENGINE=InnoDB DEFAULT CHARSET=utf8;'
            cur.execute(sql)
            print('[INFO] 已在您的 {} 資料庫中建立了 `stockList` table。'.format(self.database))

        # 將台灣上市櫃股票清單寫入 stockList table
        df.to_sql('stockList', self.engine, index=False, if_exists='append')
        print('[INFO] 台灣上市櫃股票清單已寫入資料庫中的 stockList table。')

    def queryDB(self, db, sql):
        result = self.engine.execute(sql)
        df = DataFrame(result.fetchall())
        df.columns = result.keys()

        return df