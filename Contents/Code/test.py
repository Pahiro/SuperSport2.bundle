import requests, json

session = requests.Session()

loginData = { 'email' : 'email', 
              'password' : 'password',
              'RememberMe' : 'True',
              'submit' : 'login'
    }

r = session.post('https://connect.dstv.com/4.1/en-ZA/Login', data=loginData)

#Grab the connect token
params = { 'origin' : 'https://www.supersport.com' }
r = session.get('https://connect.dstv.com/4.1/en-ZA/CrossDomainStorage/UserInfo', params=params)
tokens = json.loads(r.text)

#Resolve the user token into a Cookie
data = { 'token' : tokens['connectToken'] }
r = session.post('https://www.supersport.com/Handlers/ResolveToken.ashx', data=data)
result = json.loads(r.text)
print result['success']

params = { 'vid' : '104264' }

#Get the video source
r = session.get("https://www.supersport.com/video/playerlivejson.aspx", params=params)
result = json.loads(r.text)
print(result['result']['services']['videoURL'] + "\n") 

