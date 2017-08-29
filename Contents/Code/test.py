import re
import pyaes
import urllib, urllib2, json, cookielib
import httplib
import requests 
import auth

session = requests.Session()

response = session.post(
    'https://connect.dstv.com/4.1/en-ZA/Login',
    data={'email':'email', 'password':'password'}
)

print response.status_code #200 - Logs in Successfully

headers = { 'Host' : 'www.supersport.com',
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
            'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-US,en;q=0.5',
            'Accept-Encoding' : 'gzip, deflate, br', 
            'Connection' : 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control' : 'max-age=0' }


#Still get an auth failure.
r = session.get("https://www.supersport.com/video/playerlivejson.aspx?vid=104264", headers=headers)
#r = requests.get("https://www.supersport.com/video/playerlivejson.aspx?vid=104264", headers=headers)

print(r.text + "\n") #Working

