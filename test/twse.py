import pandas as pd
import numpy as np
import json
import requests

print('hello world')

url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20200921&stockNo=2330'
data = requests.get(url).text