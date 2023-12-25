import requests   
import time
import json
import threading
from config import Config

# Use background thread to get access token, use the following code to get access token:
# from accesstoken import AccessTokenCenter
# accessToken = AccessTokenCenter.get_access_token()
class AccessToken:
    def __init__(self):
        self.__lock = threading.Lock()

    def __real_get_access_token(self):
        api_url = Config.API_ROOT + "/api/tokens"
        resp = requests.post(api_url, data={}, auth=(Config.API_USER_NAME, Config.API_PASSWORD))
        if resp.status_code == 401:
            return '' # empty token will result in unauth error
                
        urlResp = resp.json()

        # Add new item to json
        jsonString = '{"token":"%s", "expires":%d, "time":%d}' % (urlResp['access_token'], urlResp['expires_in'], int(time.time()))
        with open(Config.ACCESS_TOKENMAP_FILENAME, "w", encoding="utf-8") as jsonFile:
            jsonFile.write(jsonString)
            jsonFile.close()
        return urlResp['access_token']

    def get_access_token(self):
        with self.__lock:
            try:
                with open(Config.ACCESS_TOKENMAP_FILENAME, encoding="utf-8") as jsonFile:
                    accessTokenMap = json.load(jsonFile)
                    jsonFile.close()
                    accessToken = accessTokenMap['token']
                    expires = accessTokenMap['expires']
                    lastTime = accessTokenMap['time']
                    timeLaps = int(time.time()) - lastTime
                    expires = expires-timeLaps

                    if expires < Config.TIMELAP:
                        return self.__real_get_access_token()
                    else:
                        jsonString = '{"token":"%s", "expires":%d, "time":%d}' % (accessToken, expires, int(time.time()))
                        with open(Config.ACCESS_TOKENMAP_FILENAME, "w", encoding="utf-8") as jsonFile:
                            jsonFile.write(jsonString)
                            jsonFile.close()

                        return accessToken
            except OSError:
                print('creating new token map file')
                return self.__real_get_access_token()
            except :
                return '' # empty token will result in unauth error
