import time
import json
from datetime import timedelta
from uuid import uuid4
from firebase_admin import messaging, credentials, initialize_app
from google.oauth2 import id_token
from google.auth.transport import requests



# TODO: need to 'remove hardcoded-fp'
service_account_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/event_backend/firebase_service_account/proximity-personal-firebase-adminsdk-ifj03-a3b8b4fe38.json'
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
  

# user_dict = {"idToken": "eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg2MTY0OWU0NTAzMTUzODNmNmI5ZDUxMGI3Y2Q0ZTkyMjZjM2NkODgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtdm5lanViN3JsbmI0Z3NsNnBta2wyb3I5cTZxZ2NlZWIuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTEwMjQ5MzcsImV4cCI6MTY1MTAyODUzN30.puE07ciDwIgP4CToyqXeYpPqDVhrrFNnZ5ssE0jb-7Eop8bn3agrxSOvbqFRG3zfiIemvoBEosXCN-Vs6jUYw5ll6Fcl70iaImcLLY2F2EvaYicXKv-Y6BWzz-QgXHPSLlerTdp71h8i4vZmke7ArYY75__Y-FhNPnfDL751mFbHjzfecU1N4r8TaOGPdP08QLoym33ZQAcYJkC3wMD4yHojjiVWoDG3ss8G3iZkVqUUov5fvbs9PyE0pr9GY__mbEjln3TKYkYzCd5yaH7YLkjhCYHXHevo95kscnVYL0TjNJ8PBclXfEjpNpWSAfRXRdcIZl0hgsLjZcXVYftHpA", "scopes": ["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"], "serverAuthCode": "null", "user": {"email": "duggalr42@gmail.com", "familyName": "Duggal", "givenName": "Rahul", "id": "115871519642305824560", "name": "Rahul Duggal", "photo": "https://lh3.googleusercontent.com/a/AATXAJwFjGR2J-5lAvvx633F9BwuA4W7kX1u0sbm-T65=s96-c"}, "user_device_token": "fygkKpTGR1ODJ40Uk88Web:APA91bEKtB-75tQVmtvoulnQ0y7PF40nQwNFLvObBZBn8TelGEF3vOl1YO-ivYsr4Gf0W29-Wtyh-7DE6VSgut-mOV7PRU0hLYjzfJSl4oFuRFm0AJGjzphP3Wds1aF03R7kN_iutN2M"}
# print(new_google_validate_token(user_dict['idToken']))

# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzMzJhYjU0NWNjMTg5ZGYxMzNlZmRkYjNhNmM0MDJlYmY0ODlhYzIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtN2txMGVudDZxdGNwdTFyZjczMWJrdmhtc2M3Y3BnNDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTA0NzYzODUsImV4cCI6MTY1MDQ3OTk4NX0.nkxs8zexcV96dWS6ueH5bWoNNRhAXj5aWES3HFRb4cq-O2L5sClJSSti2xLrgtbEw-LsTmGJ_fHJrwswQtX2NB6ucHXlWM1MskuO_x7Za2VH-gFXheTpUD9NdLLtVxGNMNpPuXhNW1LkRqrCv6ow9mhdPyS_T2VGns9BHM_L67JURP5KK_rmSg-l2u5CiMKX9TfgwT0Nbyv-BppEO5Nn5eq25WJWu0d3JFBhfYR4Gz_iU74g_yhFWgfNb5HDip4SNIWC3f5oik_IgYbAYOrCfebV_yof1_jMV5MYCAldlYfB7t6WTGmjouN6S9UeQcH1hhqk0MUvY4oCgPmXU3-dFg"
# # token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzMzJhYjU0NWNjMTg5ZGYxMzNlZmRkYjNhNmM0MDJlYmY0ODlhYzIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtN2txMGVudDZxdGNwdTFyZjczMWJrdmhtc2M3Y3BnNDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTA0NzYzODUsImV4cCI6MTY1MDQ3OTk4NX0.nkxs8zexcV96dWS6ueH5bWoNNRhAXj5aWES3HFRb4cq-O2L5sClJSSti2xLrgtbEw-LsTmGJ_fHJrwswQtX2NB6ucHXlWM1MskuO_x7Za2VH-gFXheTpUD9NdLLtVxGNMNpPuXhNW1LkRqrCv6ow9mhdPyS_T2VGns9BHM_L67JURP5KK_rmSg-l2u5CiMKX9TfgwT0Nbyv-BppEO5Nn5eq25WJWu0d3JFBhfYR4Gz_iU74g_yhFWgfNasdadb5HDip4SNIWC3f5oik_IgYbAYOrCfebV_yof1_jMV5MYCAldlYfB7t6WTGmjouN6S9UeQcH1hhqk0MUvY4oCgPmXU3-dFg"
# info = new_google_validate_token(token)
# print(info)

# tok = 'ya29.A0ARrdaM-2hlXy4pxvCYIfCViQypx6g9N6QcaU0SW_eMAqNOc-o34rdoJhj2mVk7wViKsaijhH50eqhxNvojthDHBluj42GSue1AOuvDKoQ5s6ktmo_Jh_TjA5ZcZswSB9ac2p035IO1_3xseKSHWDcJ2lz09qdA'
# get_user_info(tok)



def send_user_notification(user_tokens, type):  
  # user_tokens = ['dGziePteRsKH2GWGWp6yeM:APA91bES_afjuthXSIzI1E4KhjrWDt8NFy61dUeNZ8JocEmdkqH2Wgjo8GyGvwaG6AcOOAHHmkg_q5r-JAtgsoa4d46tvl1-cvzhjICvFpf5rQ7ntd0tbu6atQdQiADd19Ccq94rtHRJ']
  try:
    # mc_message_obj = messaging.MulticastMessage(
    #   tokens = user_tokens,
    #   data = {
    #     "notifee": json.dumps({
    #       "title": 'New Run Posted!',
    #       "body": 'Check out the New Basketball Run Posted!',
    #       "android": {
    #         "channelId": 'default',
    #         "smallIcon": 'ic_stat_sports_basketball',
    #       },
    #     }),
    #   }
    # )
    
    mc_message_obj = messaging.MulticastMessage(
      tokens = user_tokens,
      data = {
        "type": type
      }
    )
    messaging.send_multicast(mc_message_obj)
  except:
    pass


# user_tokens = ['dEz6au1XTUmkFR8EtmtEIM:APA91bEIvEjwjxWqRwcU7KMv-koVCol_npYg8xIOtjglbxNOBW6L5_Llv-A3ZjL_mnS4DlYcoAq4clmQGqBJfsnqmHrO6TaZPvJ5QgCCWCmKzgs4v3K6DFOeuDdOIgEKs28RVrb070n3']
# user_tokens = [
#   'dEz6au1XTUmkFR8EtmtEIM:APA91bEIvEjwjxWqRwcU7KMv-koVCol_npYg8xIOtjglbxNOBW6L5_Llv-A3ZjL_mnS4DlYcoAq4clmQGqBJfsnqmHrO6TaZPvJ5QgCCWCmKzgs4v3K6DFOeuDdOIgEKs28RVrb070n3',
#   'cxAFIKMGTY-pYtLvaQ3tBC:APA91bG_WkaS_YLfRcxfR4YMaBxX526-Q9Cyn-Ax0Wfy5xFM4cAZvwO6qqggbDtkF9Z9mWRUhb9bgYvBH0NMF27KyMbv_j_L6jK_h3VJUj4nvWKfj9GsSy9newaWL5dI2Crcm1gIwE9p'
# ]
# send_user_notification(user_tokens, type="event_type") 

# user_tokens = ['dGziePteRsKH2GWGWp6yeM:APA91bES_afjuthXSIzI1E4KhjrWDt8NFy61dUeNZ8JocEmdkqH2Wgjo8GyGvwaG6AcOOAHHmkg_q5r-JAtgsoa4d46tvl1-cvzhjICvFpf5rQ7ntd0tbu6atQdQiADd19Ccq94rtHRJ']
# send_user_notification(user_tokens)






