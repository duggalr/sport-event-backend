from google.oauth2 import id_token
from google.auth.transport import requests



def new_google_validate_token(token):
  CLIENT_ID = '770095547736-7kq0ent6qtcpu1rf731bkvhmsc7cpg46.apps.googleusercontent.com'
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
  


# token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzMzJhYjU0NWNjMTg5ZGYxMzNlZmRkYjNhNmM0MDJlYmY0ODlhYzIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtN2txMGVudDZxdGNwdTFyZjczMWJrdmhtc2M3Y3BnNDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTA0NzYzODUsImV4cCI6MTY1MDQ3OTk4NX0.nkxs8zexcV96dWS6ueH5bWoNNRhAXj5aWES3HFRb4cq-O2L5sClJSSti2xLrgtbEw-LsTmGJ_fHJrwswQtX2NB6ucHXlWM1MskuO_x7Za2VH-gFXheTpUD9NdLLtVxGNMNpPuXhNW1LkRqrCv6ow9mhdPyS_T2VGns9BHM_L67JURP5KK_rmSg-l2u5CiMKX9TfgwT0Nbyv-BppEO5Nn5eq25WJWu0d3JFBhfYR4Gz_iU74g_yhFWgfNb5HDip4SNIWC3f5oik_IgYbAYOrCfebV_yof1_jMV5MYCAldlYfB7t6WTGmjouN6S9UeQcH1hhqk0MUvY4oCgPmXU3-dFg"
# # token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImQzMzJhYjU0NWNjMTg5ZGYxMzNlZmRkYjNhNmM0MDJlYmY0ODlhYzIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI3NzAwOTU1NDc3MzYtNmcwZTdubWZqNzJna2k0cGlldTl2NGQzc2k3cDU1bTcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI3NzAwOTU1NDc3MzYtN2txMGVudDZxdGNwdTFyZjczMWJrdmhtc2M3Y3BnNDYuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTU4NzE1MTk2NDIzMDU4MjQ1NjAiLCJlbWFpbCI6ImR1Z2dhbHI0MkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwibmFtZSI6IlJhaHVsIER1Z2dhbCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQVRYQUp3RmpHUjJKLTVsQXZ2eDYzM0Y5Qnd1QTRXN2tYMXUwc2JtLVQ2NT1zOTYtYyIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiRHVnZ2FsIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NTA0NzYzODUsImV4cCI6MTY1MDQ3OTk4NX0.nkxs8zexcV96dWS6ueH5bWoNNRhAXj5aWES3HFRb4cq-O2L5sClJSSti2xLrgtbEw-LsTmGJ_fHJrwswQtX2NB6ucHXlWM1MskuO_x7Za2VH-gFXheTpUD9NdLLtVxGNMNpPuXhNW1LkRqrCv6ow9mhdPyS_T2VGns9BHM_L67JURP5KK_rmSg-l2u5CiMKX9TfgwT0Nbyv-BppEO5Nn5eq25WJWu0d3JFBhfYR4Gz_iU74g_yhFWgfNasdadb5HDip4SNIWC3f5oik_IgYbAYOrCfebV_yof1_jMV5MYCAldlYfB7t6WTGmjouN6S9UeQcH1hhqk0MUvY4oCgPmXU3-dFg"
# info = new_google_validate_token(token)
# print(info)

# tok = 'ya29.A0ARrdaM-2hlXy4pxvCYIfCViQypx6g9N6QcaU0SW_eMAqNOc-o34rdoJhj2mVk7wViKsaijhH50eqhxNvojthDHBluj42GSue1AOuvDKoQ5s6ktmo_Jh_TjA5ZcZswSB9ac2p035IO1_3xseKSHWDcJ2lz09qdA'
# get_user_info(tok)





