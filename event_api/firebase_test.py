import time
import json
from datetime import timedelta
from uuid import uuid4

from firebase_admin import messaging, credentials, initialize_app




# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/Users/rahul/Documents/main/projects/personal_learning_projects/event_backend/firebase_service_account/proximity-personal-firebase-adminsdk-ifj03-a3b8b4fe38.json'


service_account_fp = '/Users/rahul/Documents/main/projects/personal_learning_projects/event_backend/firebase_service_account/proximity-personal-firebase-adminsdk-ifj03-a3b8b4fe38.json'
cred = credentials.Certificate(service_account_fp)
initialize_app(cred)
user_tokens = ['dGziePteRsKH2GWGWp6yeM:APA91bES_afjuthXSIzI1E4KhjrWDt8NFy61dUeNZ8JocEmdkqH2Wgjo8GyGvwaG6AcOOAHHmkg_q5r-JAtgsoa4d46tvl1-cvzhjICvFpf5rQ7ntd0tbu6atQdQiADd19Ccq94rtHRJ']
mc_message_obj = messaging.MulticastMessage(
  tokens = user_tokens,
  data = {
    "notifee": json.dumps({
      "title": 'New Run Posted!',
      "body": 'Check out the New Basketball Run Posted!',
      "android": {
        "channelId": 'default',
        "smallIcon": 'ic_stat_sports_basketball',
      },
    }),
  }
)
messaging.send_multicast(mc_message_obj)
 



# firebaseApp = initialize_app()
# print(firebaseApp)
# user_tokens = ['dGziePteRsKH2GWGWp6yeM:APA91bES_afjuthXSIzI1E4KhjrWDt8NFy61dUeNZ8JocEmdkqH2Wgjo8GyGvwaG6AcOOAHHmkg_q5r-JAtgsoa4d46tvl1-cvzhjICvFpf5rQ7ntd0tbu6atQdQiADd19Ccq94rtHRJ']
# mc_message_obj = messaging.MulticastMessage(
#   tokens = user_tokens,
#   data = { 'hello': 'world!' } 
# )
# messaging.send_multicast(mc_message_obj)





# print(credentials.ApplicationDefault.get_credential())

# config = {
#   "apiKey": "AIzaSyAR8j4JsjCf4YlxDuS1eXDkrwlm58ojoSk",
#   "projectId":  "proximity-personal",
#   "storageBucket": "proximity-personal.appspot.com",
#   "appId": "1:770095547736:android:28091df2a3ae7f3794d12d",

# }
# firebaseApp = initialize_app(config)
# print(firebaseApp)
# user_tokens = ['dGziePteRsKH2GWGWp6yeM:APA91bES_afjuthXSIzI1E4KhjrWDt8NFy61dUeNZ8JocEmdkqH2Wgjo8GyGvwaG6AcOOAHHmkg_q5r-JAtgsoa4d46tvl1-cvzhjICvFpf5rQ7ntd0tbu6atQdQiADd19Ccq94rtHRJ']
# mc_message_obj = messaging.MulticastMessage(
#   tokens = user_tokens,
#   data = { 'hello': 'world!' } 
# )
# messaging.send_multicast(mc_message_obj)



# __all__ = ['send_to_firebase', 'update_firebase_snapshot']

# initialize_app()

# def send_to_firebase(raw_notification):
#  db = firestore.client()
#  start = time.time()
 
# db.collection('notifications').document(str(uuid4())).create(raw_notification)
#  end = time.time()
#  spend_time = timedelta(seconds=end - start)
#  return spend_time


# def update_firebase_snapshot(snapshot_id):
#  start = time.time()
#  db = firestore.client()
#  db.collection('notifications').document(snapshot_id).update(
#     {'is_read': True}
#  )
#  end = time.time()
#  spend_time = timedelta(seconds=end - start)
#  return spend_time

# export GOOGLE_APPLICATION_CREDENTIALS='/Users/rahul/Documents/main/projects/personal_learning_projects/event_app/android/app/google-services.json'



