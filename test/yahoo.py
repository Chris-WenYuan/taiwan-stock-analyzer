import time
import requests

from bs4 import BeautifulSoup

class Stock:
    # Constructor
    def __init__(self, *stock_numbers):
        self.stock_numbers = stock_numbers
        print(self.stock_numbers)
    
    # Crawl
    def scrape(self):
        result = list()
        

        for stock_numbers in self.stock_numbers:
            # https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=%E6%B0%B4%E6%B3%A5&form=menu&form_id=stock_id&form_name=stock_name&domain=0
            response = requests.get('https://tw.stock.yahoo.com/q/q?s=' + stock_numbers)
            soup = BeautifulSoup(response.text.replace('加到投資組合', ''), 'lxml')

            stock_date = soup.find('font', {'class', 'tt'}).getText().strip()[-9:]

            tables = soup.find_all('table')[2]
            tds = tables.find_all('td')[0:11]

            result.append((stock_date,) + tuple(td.getText().strip() for td in tds))

            time.sleep(3)

        return result

count = 0
stock = Stock('2451', '2454', '5351')
print(stock.scrape())
count += 6
print('Current cost ' + str(count) + ' (seconds)\n')
