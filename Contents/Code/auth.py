import requests
#import grequests
import json

loginurl  = "https://connect.dstv.com/4.1/en-ZA/Login"

session = requests.Session()

def login():
    global session
    
    username = Prefs["email"]
    password = Prefs["password"]
    
    loginData = { 
        'email' : username, 
        'password' : password,
        'RememberMe' : 'True',
        'submit' : 'login'
    }
    
    Log("Loading login page...")
    r = session.post('https://connect.dstv.com/4.1/Login', 
                       data=loginData)
    resolveToken(grabToken())
    #grequests.send(r, grequests.Pool(1))



def grabToken():
    global session
    
    #Grab the connect token
    params = { 'origin' : 'https://www.supersport.com' }
    r = session.get('https://connect.dstv.com/4.1/en-ZA/CrossDomainStorage/UserInfo', params=params)
    if r.status_code == 200:
        Log("Token retrieved")
    result = json.loads(r.text)
    return result
    
def resolveToken(result):
    global session
    
    #Resolve the user token into a Cookie
    data = { 'token' : result['connectToken'] }
    r = session.post('https://www.supersport.com/Handlers/ResolveToken.ashx', data=data)
    result = json.loads(r.text)
    if result['success'] == 'true':
        Log('Cookie generated for session')
