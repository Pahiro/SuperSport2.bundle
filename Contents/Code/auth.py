import requests
import json
import cookielib

loginurl  = "https://connect.dstv.com/4.1/en-ZA/Login"
session = requests.Session()
token = None
#cookie_file = 'cookie.txt'
#cj = cookielib.LWPCookieJar(cookie_file)

#try:
#    cj.load()
#except:
#    pass

#session.cookies = cj

def login():
    global session, cj
    
    username = Prefs["email"]
    password = Prefs["password"]
    
    loginData = { 
        'email' : username, 
        'password' : password,
        'RememberMe' : 'True',
        'submit' : 'login'
    }
    
    Log("Loading login page...")
    session.post('https://connect.dstv.com/4.1/Login', 
                data=loginData)
    r = grabToken()
    resolveToken(r)
    
    

def grabToken():
    global session, token
    
    #Grab the connect token
    params = { 'origin' : 'https://www.supersport.com' }
    r = session.get('https://connect.dstv.com/4.1/en-ZA/CrossDomainStorage/UserInfo', 
                    params=params)
    if r.status_code == 200:
        Log("Token Retrieved")
    try:
        result = json.loads(r.text)
    except: 
        print r.reason
    
    token = result['connectToken']
    
    return result
    
def resolveToken(result):
    global session
    
    #Resolve the user token into a Cookie
    data = { 'token' : result['connectToken'] }
    r = session.post('https://www.supersport.com/Handlers/ResolveToken.ashx', 
                     data=data)
    result = json.loads(r.text)
    Log("Token resolved into cookie")
