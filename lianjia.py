# coding: utf-8
import requests
from bs4 import BeautifulSoup
import re
import pandas

def getHtml(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.text
    except:
        print("未能获取")

def getDetail(html):
    soup = BeautifulSoup(html, 'lxml')
    info = soup.select('.info.clear')
    try:
        for item in info:
            address = item.select('.address')[0].get_text().split('|'),
            local = address[0]
            flood = item.select('.flood')[0].get_text().split('-')
            unitPrice = item.select('.unitPrice')[0].get_text()
            yield {
                'href': item.select('a')[0]['href'],
                'title': item.select('.title')[0].get_text(),
                'address-a': local[0],
                'address-b': local[1],
                'address-c(平米)': float(local[2][:-3]),
                'address-d': local[3],
                'address-e': local[4],
                'flood-1': flood[0],
                'flood-2': flood[1],
                'followInfo': item.select('.followInfo')[0].get_text(),
                'totalPrice(万)': float(item.select('.totalPrice')[0].get_text().rstrip('万')),
                'unitPrice（元/平米）': float(re.search('(\d+)', unitPrice, re.S).group(1))
            }
    except:
        print("无返回")


if __name__ == '__main__':
    url = 'https://cs.lianjia.com/ershoufang/'
    html = getHtml(url)
    total = re.search('totalPage":(.*?),', html, re.S)
    page_total = int(total.group(1))
    l = []
    base_url = 'https://cs.lianjia.com/ershoufang/pg'
    for num in range(1, page_total + 1):
        html = getHtml(base_url + str(num))
        detail = getDetail(html)
        for i in detail:
            l.append(i)
    df = pandas.DataFrame(l)
    df.to_excel('result.xlsx')
