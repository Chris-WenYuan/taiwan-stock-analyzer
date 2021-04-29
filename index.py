import curses, time
from pandas import set_option
from taiwan_stock import crawler

# 使 dataframe 輸出中文字時也能對齊
set_option('display.unicode.ambiguous_as_wide', True)
set_option('display.unicode.east_asian_width', True)

if __name__ == '__main__': 
    df = crawler.getStockList() # 取得台灣上市上櫃股票清單

    # -----------------------------------------------------------
    # 關於 crawler.getAllStockHistory()
    # -----------------------------------------------------------
    # 根據 crawler.getStockList 回傳的 dataframe 來抓取個股歷史紀錄
    # -----------------------------------------------------------
    # 市場別 (markets) 共有 2 種：
    #   1. '上市'
    #   2. '上櫃'
    # -----------------------------------------------------------
    # 個股類型 (types) 共有 9 種：
    #   1. '股票'
    #   2. '臺灣存託憑證(TDR)'
    #   3. 'ETF'
    #   4. 'ETN'
    #   5. '特別股'
    #   6. '受益證券-不動產投資信託'
    #   7. '受益證券-資產基礎證券'
    #   8. '上市認購(售)權證'
    #   9. '上櫃認購(售)權證'
    # -----------------------------------------------------------
    # markets = ['上市', '上櫃']
    # types = ['股票', '臺灣存託憑證(TDR)', 'ETF', 'ETN']
    markets = ['上市', '上櫃']
    types = ['臺灣存託憑證(TDR)']
    crawler.getAllStockHistory(df, markets, types)

    sid = ['2330', '2886']
    result_df = crawler.getRealTime(sid)