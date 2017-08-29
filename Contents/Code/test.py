import re
import pyaes
import urllib, urllib2, json, cookielib
import httplib
import requests 
import auth

LIVE_STREAMS_URL = "https://www.supersport.com/AjaxOperation.aspx/GetVideoStreams"

auth.login()
cookie = auth.check_auth()

if cookie == False:
    cookie = auth.login()
for item in cookie:    
    headers = { 'Host' : 'www.supersport.com',
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language' : 'en-US,en;q=0.5',
                'Accept-Encoding' : 'gzip, deflate, br',
                'Cookie' : item.name + '=' + item.value, 
                'Connection' : 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control' : 'max-age=0' }


r = requests.get("https://www.supersport.com/video/playerlivejson.aspx?vid=104264", headers=headers, cookies=cookie)

print(r.text + "\n") #Working

