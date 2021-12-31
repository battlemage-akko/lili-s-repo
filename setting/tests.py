from django.test import TestCase
from fake_useragent import UserAgent
import requests
useragent = UserAgent().chrome

headers = {
    'user-agent':useragent
}
data = {'page':'2'}

response = requests.post(url='https://www.hpoi.net/user/home/ajax',headers=headers)
print(response.text)
# Create your tests here.

