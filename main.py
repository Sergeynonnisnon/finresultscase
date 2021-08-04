"""
Ниже есть ссылки на документы.
 К каждой ссылки есть 2-3 значения, которые нужно найти в тексте дока и спарсить.
 Также к каждой ссылке есть скрины места в тексте, где оно встречалось.
 (Эти значения могут встретиться и в других местах)
Задача написать скриптец/проектик (можно и в джупитере),
 который бы скрапил по ссылке каждый док и регулярками
 (максимально универсальными, так чтоб одно выражение покрывало
 все кейсы для одного значения) парсить док. Выводить результат можно хоть на экран)
Ограничения: юзай питон3 и все его библиотеки
Выполнения оформи на гитхабе и кидай линку.

Link:https://sec.report/Document/0001193125-21-072571/
IPO Price: 11.50$
Number Shares: 12,218,750
IPO Unit: 10$

Link: https://sec.report/Document/0001193125-21-031547/
Number Shares: 8,500,000
IPO Price: 22-24$

Link: https://sec.report/Document/0001193125-21-024746/
IPO Price: 15-17$
Number Shares: 6,250,000

Link: https://sec.report/Document/0001193125-21-056708/
IPO Price: 32-34$
Number Shares: 31,000,000
"""

from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as BS
import re

links = ('https://sec.report/Document/0001193125-21-072571/',
         'https://sec.report/Document/0001193125-21-031547/',
       'https://sec.report/Document/0001193125-21-024746/',
       'https://sec.report/Document/0001193125-21-056708/')


def get_html(url):
    ua = UserAgent()

    header = {'User-Agent': str(ua.chrome)}

    #url = 'https://sec.report/Document/0001193125-21-031547/'
    response = requests.get(url, headers=header)
    soup = BS(response.text, "lxml")
    return soup

if __name__=='__main__':
    for i in links:
        print(i)

        soup = get_html(i)

        IPO_price = soup.find_all(text=re.compile("\sbetween\s(\$\d\d.\d\d)\sand\s|(\$\d\d.\d\d)+ per share"), limit=1)[
            0]
        IPO_price = re.findall("(\$\d\d.\d\d)", IPO_price)
        print(f'IPO price is {IPO_price}')
        shares = soup.find_all(text=re.compile("^(\d.*)\s\dhares|(\d{2,3},\d{3},\d{3})\sClass\sA\sordinary shares"))

        shares = re.findall(
            "Redeemable warrants included as part of the units.{6}\s{3}(\d{2,3},\d{3},\d{3})|(\d{1,3},\d{3},\d{3})\s\whares\s\s",
            soup.get_text())[0]

        for i in shares:
            if len(i) > 1:
                shares = i
                break
        print(f"Number Shares is {shares}")

        try:
            IPO_unit = re.findall("price\sof\s\$(\d{1,2}[.,]\d{2})\sper\sunit", soup.get_text())[0]
            print(f'IPO UNIT IS {IPO_unit}')
        except IndexError:
            print('no info about ipo unit')
