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








