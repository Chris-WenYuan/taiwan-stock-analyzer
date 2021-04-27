from taiwan_stock import crawler

if __name__ == '__main__':
    df = crawler.getStockList()

    result_df = df[df['類型']=='股票']
    sid = list(result_df.index)
    listed_date = df['上市日'].tolist()

    crawler.getAllStockHistory(sid, listed_date)