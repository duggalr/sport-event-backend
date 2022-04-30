import os
import time
import json
from datetime import timedelta
from uuid import uuid4
from firebase_admin import messaging, credentials, initialize_app
from google.oauth2 import id_token
from google.auth.transport import requests



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
service_account_fp = os.path.join(BASE_DIR, 'firebase_service_account/proximity-personal-firebase-adminsdk-ifj03-a3b8b4fe38.json')
cred = credentials.Certificate(service_account_fp)
initialize_app(cred)


def new_google_validate_token(token):
  # CLIENT_ID = '770095547736-7kq0ent6qtcpu1rf731bkvhmsc7cpg46.apps.googleusercontent.com'
  CLIENT_ID = '770095547736-vnejub7rlnb4gsl6pmkl2or9q6qgceeb.apps.googleusercontent.com'
  # Specify the CLIENT_ID of the app that accesses the backend:
  try: 
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
   
    return True, idinfo
  except:
    return False, None
  

google_access_token_url = 'https://www.googleapis.com/oauth2/v3/userinfo?access_token='

def get_user_info(user_tok):
  import requests
  final_url = google_access_token_url + user_tok
  res = requests.get(final_url)
  return res.json()
  

def send_user_notification(user_tokens, type):  
  try:
    mc_message_obj = messaging.MulticastMessage(
      tokens = user_tokens,
      data = {
        "type": type
      }
    )
    messaging.send_multicast(mc_message_obj)
  except:
    pass


# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2MTY0OWU0NTAzMTUzODNmNmI5ZDUxMGI3Y2Q0ZTkyMjZjM2NkODgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtdm5lanViN3JsbmI0Z3NsNnBta2wyb3I5cTZxZ2NlZWIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTEyODM5MzcsImV4cCI6MTY1MTI4NzUzN30.Xqy0zNg4J0pYYo_EyuaETArU5iDEp2F_u5_GHXtwOuVRdc5MfPGae_4TV-MABHc7l3ziTXGToikJnQNqPf--BRrtGidbYbgE-wXHFgpfgs89RUOY27OEI8GrCEqGVPZKecRZiY5PVaQBXWDBL7i__NM4WCP-UFMeh6nRwvqV9fWEEzNE6d7QU3CHN0211WIXkDDBGVhc6e7LR6E3sHyf8IUmDUr6sSzLaAIV0Az3xqCfzdoTSOo6_4kvcQ9---Z8VL5BevK4S2-bn1GZnhKRuQQeqfP9h7sENMoNmgBJHl56EJgPkPoZhwmRsQWHRLPlmo5ietRLfmYcM6fjXU_ZqQ"
# print(new_google_validate_token(token))

# user_tokens = ['eYsJhWhRT12-5tVw2t2SXq:APA91bGnXHStCUGTmdQIKGlhXgbeQScxh8rOJZ6kDE7Gimf4pSsWKxAHeMcyClwgDg_nR9LknLoKiM7KpmAg3sBTU-Olep9EZxqxEsI0K5mrUm5XPHReWMUDT4LCjB1hb-TbNrmVhGf-']
# send_user_notification(user_tokens, type='create_event')







