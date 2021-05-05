# 台灣上市上櫃股票分析

這是一個台灣上市上櫃股票分析的專案，預計會將股票的基本面、技術面、籌碼面、消息面以及各種財經新聞納入分析之考量，以過去經驗推測一檔股票未來的漲跌勢。此專案之工作量龐大，估計在工作之餘使用兩年時間完成。

## 當前專案進度

- 抓取台灣上市櫃股票清單，並儲存在 `./output/股票列表/stockList.csv` (2021/05/04)
- 根據指定市場別及股票類型來抓取每檔股票的歷史紀錄，並儲存在 `./output/歷史紀錄/` (2021/05/04)

## 使用步驟

使用 `git clone` 指令下載本專案。

```shell
$ git clone https://github.com/Chris-WenYuan/taiwan-stock-analyzer.git
```

使用 `cd` 進入專案資料夾中。

```shell
$ cd taiwan-stock-analyzer
./taiwan-stock-analyzer$ 
```

利用 `requirements.txt` 安裝相關套件。

```shell
(taiwan-stock-analyzer)$ pip install -r requirements.txt
```

`index.py` 為本專案的主程式，直接執行即可。

```shell
(taiwan-stock-analyzer)$ python index.py
```

![](https://i.imgur.com/ce1TRnc.png)

## 參考資料

- [台灣證券交易所](https://www.twse.com.tw/zh/)
- [Yahoo奇摩股市](https://tw.stock.yahoo.com/)
- [Anue鉅亨網](https://www.cnyes.com/)
- [證券櫃檯買賣中心](https://www.tpex.org.tw/web/)