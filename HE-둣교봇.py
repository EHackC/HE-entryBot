import requests,logging,time
from logging.config import dictConfig
from datetime import datetime

cookies={}

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(message)s',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logfile.log',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['file']
    }
})


def currentMilliTime():
    return round(time.time()*1000)

def Erequests(data):
    global cookies
    r=requests.post("https://playentry.org/graphql",data=(data).encode("utf-8"),headers={"Content-Type":"application/json; charset=utf-8"},cookies=cookies)
    logging.debug("!FUNC-Erequests!~(success)-"+data)
    cookies=r.cookies.get_dict()
    return r.json()

logging.debug("!MAIN!~(success)-start")
print("설정 가져오는중..")
with open("setting.txt","r",encoding="utf-8") as f:
    setting=f.read().split("\n")
print("로그인중..")
loginData=Erequests("{\"query\":\"mutation($username:String!,$password:String!,$rememberme:Boolean,$captchaValue:String,$captchaKey:String,$captchaType:String){signinByUsername(username:$username,password:$password,rememberme:$rememberme,captchaValue:$captchaValue,captchaKey:$captchaKey,captchaType:$captchaType){id nickname role isEmailAuth}}\",\"variables\":{\"username\":\""+setting[1]+"\",\"password\":\""+setting[4]+"\"}}")
if loginData["data"]["signinByUsername"]!=None:
    print("로그인 성공!")
    logging.debug("!MAIN!~(success)-login")
    if setting[7]=="1":
        logging.debug("!MAIN!~(success)-start bot,type1")
        lastTime=0
        while 1:
            time.sleep(0.1)
            if currentMilliTime()%int(setting[10])<=2000:
                if currentMilliTime()-lastTime>2000:
                    lastTime=currentMilliTime()
                    Erequests("{\"query\":\"mutation CREATE_ENTRYSTORY($content:String$text:String$image:String$sticker:String$cursor:String){createEntryStory(content:$content text:$text image:$image sticker:$sticker cursor:$cursor){warning}}\",\"variables\":{\"content\":\"["+str(datetime.now().hour)+":"+str(datetime.now().minute)+"]"+setting[13]+"\"}}")
                    print("글 업로드:["+str(datetime.now().hour)+":"+str(datetime.now().minute)+"]"+setting[13])
                    logging.debug("!MAIN!~(success)-upload")
else:
    print("로그인에 실패하였습니다.")
    logging.debug("!MAIN!~(failed)-login")
