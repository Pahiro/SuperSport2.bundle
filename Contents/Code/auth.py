#import re
import urllib
import requests 

loginurl  = "https://connect.dstv.com/4.1/en-ZA/Login"
memberurl = "https://connect.dstv.com/4.1/en-ZA/Overview/"

username = Prefs["email"]
password = Prefs["password"]

headers = {
  'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
  'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml; q=0.9,*/*; q=0.8',
  'Content-Type': 'application/x-www-form-urlencoded'
}


####################################################################################################
# Does the login and opens some link
def login():
    loginData = urllib.urlencode(
    { 
        'email' : username,
        'password' : password,
        'RememberMe' : True,
        'submit' : 'login'
    })
    
    r  = requests.post(loginurl, loginData)    
    return r.cookies

def account_check(html):
    if html.find('<span class="username">') == None:
        return False
    else:
        return True

def check_auth():
    if username != '' and password != '':
        r = requests.get(memberurl)
        if (account_check(r.text) == False):
            return False
        else:
            print ("Logged in" + "\n")
            return r.cookies
    else:
        return False
