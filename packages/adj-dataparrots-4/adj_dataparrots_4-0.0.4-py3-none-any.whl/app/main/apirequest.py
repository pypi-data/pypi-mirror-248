import requests
from config import Config
from app.access_token import AccessToken
from app.app_log import app_log
    
def request_post(url, data=None):
    api_url = Config.API_ROOT + url
    token = AccessToken().get_access_token()
    headers = {'Authorization': "Bearer {}".format(token)}
    return requests.post(api_url, json=data, headers=headers).json()
