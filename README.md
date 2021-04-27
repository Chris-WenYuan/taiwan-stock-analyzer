# 台灣股票分析專案

這是一個台灣上市上櫃股票分析的專案，預計會將股票的基本面、技術面、籌碼面、消息面以及各種財經新聞納入分析之考量，以過去經驗推測一檔股票未來的漲跌勢。此專案之工作量龐大，估計在工作之餘使用兩年時間完成。

## 當前專案進度

1. 抓取台灣上市上櫃的股票清單並存入自建的 MySQL 資料庫 (20210426)
2. 根據抓到的台灣上市上櫃股票清單去爬每支股票的歷史紀錄 (未完成)

## 使用步驟

### 一、安裝 MySQL

可以參考[這篇文章](https://andy6804tw.github.io/2019/01/29/ubuntu-mysql-setting/)在 Ubuntu 系統上安裝 MySQL。安裝完畢後再參考[這篇文章](https://www.opencli.com/mysql/mysql-add-new-users-databases-privileges)來創建 MySQL 使用者和資料庫(`host`, `user`, `password`, `database`)以供之後程式使用。

### 二、執行程式

打開 `index.js` 檔案，並找到下面這行程式碼，其中的 `host`、`user`、`password`、`database` 參數是我本地端 MySQL 資料庫的設定，你需要依你自己的設定去更改。

```python
ms.connectDB(host='localhost', user='chris', password='850806', database='stock')
```

修改完後可以執行以下指令來運行程式。

```shell
$ python index.js
```