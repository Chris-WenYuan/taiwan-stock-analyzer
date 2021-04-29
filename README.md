# 台灣上市上櫃股票分析

這是一個台灣上市上櫃股票分析的專案，預計會將股票的基本面、技術面、籌碼面、消息面以及各種財經新聞納入分析之考量，以過去經驗推測一檔股票未來的漲跌勢。此專案之工作量龐大，估計在工作之餘使用兩年時間完成。

## 當前專案進度

1. 抓取台灣上市上櫃的股票清單並儲存為 /data/stockList.csv (20210426)
2. 根據抓到的股票清單去爬上面每支股票的歷史紀錄並存入 /data/hostory/ (20210428)

## 使用步驟

使用 `git clone` 指令下載本專案。

```shell
$ git clone https://github.com/Chris-WenYuan/taiwan-stock-analyzer.git
```

使用 `cd` 進入專案資料夾中。

```shell
$ cd taiwan-stock-analyzer
(taiwan-stock-analyzer)$ 
```

利用 `requirements.txt` 安裝相關套件。

```shell
(taiwan-stock-analyzer)$ pip install -r requirements.txt
```

`index.py` 為本專案的主程式，直接執行即可。

```shell
(taiwan-stock-analyzer)$ python index.py
```

![](https://i.imgur.com/xlMXK0p.png)
