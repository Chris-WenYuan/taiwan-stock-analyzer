from pandas import set_option
from taiwan_stock import crawler

# 使 dataframe 輸出中文字時也能對齊
set_option('display.unicode.ambiguous_as_wide', True)
set_option('display.unicode.east_asian_width', True)

if __name__ == '__main__': 
    df = crawler.getStockList() # 取得台灣上市上櫃股票清單並儲存在 /output/stockList.csv
    
    # -----------------------------------------------------------
    # crawler.getAllStockHistories() 使用教學
    # -----------------------------------------------------------
    # 根據 crawler.getStockList 回傳的 dataframe 來抓取個股歷史紀錄
    # -----------------------------------------------------------
    # 市場別 (markets) 共有 2 種：
    #   1. '上市'
    #   2. '上櫃'
    # -----------------------------------------------------------
    # 個股類型 (types) 共有 7 種：
    #   1. '股票'
    #   2. '臺灣存託憑證(TDR)'
    #   3. 'ETF'
    #   4. 'ETN'
    #   5. '特別股'
    #   6. '受益證券-不動產投資信託'
    #   7. '受益證券-資產基礎證券'
    # -----------------------------------------------------------
    # crawler.getAllStockHistories(df, markets, types) 之參數
    # df = crawler.getStockList()
    # markets = ['上市', '上櫃']
    # types = ['股票', '臺灣存託憑證(TDR)', 'ETF', 'ETN', '特別股',
    #          '受益證券-不動產投資信託', '受益證券-資產基礎證券']
    # -----------------------------------------------------------
    markets = ['上市', '上櫃']
    types = ['股票', '臺灣存託憑證(TDR)', 'ETF', 'ETN', '特別股', '受益證券-不動產投資信託', '受益證券-資產基礎證券']
    crawler.getAllStockHistories(df, markets, types) # 根據指定的市場別(markets)和股票類型(types)來抓取其所有個股之歷史股價(從 2017-02-06 開始)，並儲存至 /output/歷史股價/
