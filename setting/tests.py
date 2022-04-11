from django.test import TestCase
from fake_useragent import UserAgent
from lxml import etree as e
import requests
headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

baseUrl = 'https://www.hpoi.net/'

response = requests.get(url='https://www.hpoi.net/user/home?type=info',headers=headers)

print(response.text)
html = e.HTML(response.text)

result = html.xpath("//div[@class='user-content']/text()")

lastId = html.xpath("//div[@class='main-content']/input/@value")

urls = html.xpath("//div[@class='col-xs-8 overlay-container']/a/@href")

union = []

for i in zip(result,urls):
    tmp = []
    tmp.append(i[0])
    tmp.append(baseUrl + i[1])
    union.append(union)
    print(tmp)
print('----------------------------------------------------------------------------------------------------------------------------------')
for i in range(20):
    data = {
        'page': i+2,
        'type': 'info',
        'lastId': lastId
    }

    responseAjax = requests.post(url='https://www.hpoi.net/user/home/ajax', headers=headers, data=data)

    htmlAjax = e.HTML(responseAjax.text)

    result = htmlAjax.xpath("//div[@class='user-content']/text()")

    lastId = htmlAjax.xpath("//input/@value")

    urls = htmlAjax.xpath("//div[@class='col-xs-8 overlay-container']/a/@href")

    for i in zip(result, urls):
        tmp = []
        tmp.append(i[0])
        tmp.append(baseUrl + i[1])
        union.append(union)
        print(tmp)
    print('----------------------------------------------------------------------------------------------------------------------------------')
# Create your tests here.

