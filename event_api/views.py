from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

import datetime
import json
from django.http import JsonResponse

from . import utils
from .models import UserProfile, EventDetail, UserGoingEvent, EventComments




park_address_info = {
  'Kipling Parkette': '7550 Kipling Avenue, Woodbridge, ON',
  'Smithfield Park': '173 Mt Olive Dr, Etobicoke, ON',
  'Waterfront Neighbourhood Centre': '627 Queens Quay W, Toronto, ON',
  'David Crombie Park': '115 Scadding Ave, Toronto, ON',
  'Underpass Park': '29 Lower River Street, Toronto, ON',
  'Flagstaff Park': '42 Mercury Rd, Etobicoke, ON',
  'Indian Line Park': '655 HUMBERWOOD BLVD',
  'Summerlea Park': '2 Arcot Blvd, Toronto, ON',
  'Firgrove Park': '254 Firgrove Crescent, North York, ON',
  'Stanley Greene Park': 'Stanley Greene Blvd, Toronto, ON',
  'Irving W. Chapley Park': '205 Wilmington Ave, North York, ON',
  'McNicoll Park': '215 McNicoll Ave, North York, ON',
  'Sanwood Park': '20 Sanwood Blvd, Scarborough, ON',
  'Confederation Park': '250 Dolly Varden Blvd, Scarborough, ON',
  'MacGregor Playground': '346 LANSDOWNE AVE, Toronto, ON',
  'Jack Goodlad Park': '929 Kennedy Rd, Scarborough, ON',
  'Ramsden Park': '1020 Yonge St & Ramsden Park Rd, Toronto, ON',
  'Christie Pits Park': '750 Bloor St W, Toronto, ON',
  'Earlscourt Park': '1200 LANSDOWNE AVE, Toronto, ON',
  'Ourland Park': '36 Ourland Ave, Etobicoke, ON',
  'Paul Coffey Park': '3430 Derry Rd E, Mississauga, ON',
  'Regent Park Athletic Grounds': '480 Shuter St, Toronto, ON'
}

time_mapping = {
  '1:00': '13:00', 
  '2:00': '14:00',
  '3:00': '15:00',
  '4:00': '16:00',
  '5:00': '17:00',
  '6:00': '18:00',
  '7:00': '19:00',
  '8:00': '20:00',
  '9:00': '21:00'
}

reverse_time_mapping = {v: k for k, v in time_mapping.items()}




def validate_user(json_data):
  if 'access_token' in json_data:
    user_access_token = json_data['access_token']
    access_token_res = utils.get_user_info(user_access_token)

    if 'error' not in access_token_res:
      if 'sub' in access_token_res:
        user_profile_id = access_token_res['sub']
        user_objects = UserProfile.objects.filter(google_profile_id=user_profile_id)
        if len(user_objects) == 1:
          return True, user_objects[0] 

  return False, None



@csrf_exempt
@require_POST
def update_user_device_token(request):
  try:
    json_data = json.loads(request.body)
    valid_user, user_obj = validate_user(json_data)
    if valid_user:
      tok = json_data['userDeviceToken']
      user_obj.phone_device_token = tok
      user_obj.save()
      return JsonResponse({'success': True})
    else:
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})
  
  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})


@csrf_exempt
@require_POST
def auth_signup(request):
  """
  save user profile info from Google 
    -validate user-idToken; if valid, get the associated data and save
  """
  try: 
    json_data = json.loads(request.body) 

    if 'idToken' in json_data:
      user_tok = json_data['idToken']
      valid, user_data = utils.new_google_validate_token(user_tok)

      if valid: 
        user_google_id = user_data['sub']
        user_objects = UserProfile.objects.filter(google_profile_id=user_google_id)
        
        if len(user_objects) == 0:
          user_email = user_data['email']
          user_full_name = user_data['name']
          user_profile_pic_url = user_data['picture']
          user_first_name = user_data['given_name']
          user_last_name = user_data['family_name']
          user_device_token = None
          if 'user_device_token' in json_data:
            user_device_token = json_data['user_device_token']

          u = UserProfile.objects.create(
            google_profile_id=user_google_id,
            first_name=user_first_name,
            last_name=user_last_name,
            full_name=user_full_name,
            email=user_email,
            profile_picture_url=user_profile_pic_url,
            phone_device_token=user_device_token
          )
          u.save()

          return JsonResponse({'success': True})

        else: 
          return JsonResponse({'success': False, 'reason': 'invalid data sent.'})      

      else: 
        return JsonResponse({'success': False, 'reason': 'invalid token sent.'})
        
    else: 
      return JsonResponse({'success': False, 'reason': 'invalid token sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def create_event(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)

    if valid_user:  
      event_title = json_data['event_title']
      event_desc = json_data['event_description']
      park_name = json_data['park_name']
      park_address = park_address_info[park_name]
      event_date = json_data['event_date'].split('T')[0]
      event_time = json_data['event_time']
      time_str_repres = time_mapping[event_time]
      time_dt_repres = datetime.datetime.strptime(time_str_repres, '%H:%M').time()

      ed = EventDetail.objects.create(
        event_title = event_title,
        park_name = park_name,
        park_address = park_address,
        event_description = event_desc,
        event_date = event_date,
        event_time = time_dt_repres,
        user_obj = user_obj
      )
      ed.save()

      ug = UserGoingEvent.objects.create(
        user_obj = user_obj,
        event_obj = ed
      )
      ug.save()
        
      # get all user-device-tokens except for current user
      notification_device_tokens = [] 
      all_user_objects = UserProfile.objects.all()
      for a_user_obj in all_user_objects:
        if a_user_obj.phone_device_token != '' and a_user_obj != user_obj:
          notification_device_tokens.append(a_user_obj.phone_device_token)

      utils.send_user_notification(notification_device_tokens, type='create_event')
      return JsonResponse({'success': True})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except: 
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def get_events(request):
  today = datetime.datetime.today()
  event_objects = EventDetail.objects.filter(event_date__gte=today).order_by('event_date')
  user_going_objects = UserGoingEvent.objects.all()

  event_id_dict = {}
  event_id_comment_dict = {}
  final_list = []
  for ev_obj in event_objects:
    user_going_objects = UserGoingEvent.objects.filter(event_obj=ev_obj)
    user_going_list = []
    for ug_obj in user_going_objects:
      user_going_list.append({'ug_id': ug_obj.id, 'profile_picture': ug_obj.user_obj.profile_picture_url, 'name': ug_obj.user_obj.full_name})
    
    orig_event_time = ev_obj.event_time
    st_orig_event_time = orig_event_time.strftime("%H:%M")
    event_time_st = reverse_time_mapping[st_orig_event_time] + 'PM'

    event_comments = EventComments.objects.filter(event_obj=ev_obj)
    event_comments_list = []
    for ec_obj in event_comments:
      event_comments_list.append({
        'user_full_name': ec_obj.user_obj.full_name,
        'user_profile_pic': ec_obj.user_obj.profile_picture_url,
        'comment': ec_obj.comment_text
        })    

    final_di = {
      'event_id': ev_obj.id,
      'event_name': ev_obj.event_title.capitalize(), 
      'event_description': ev_obj.event_description, 
      'park_name': ev_obj.park_name,
      'park_address': ev_obj.park_address,
      'event_date': ev_obj.event_date,
      'event_time': event_time_st,
      'user_going_list': user_going_list,
      'user_event_comments': event_comments_list,
    }
    final_list.append(final_di)
    event_id_dict[ev_obj.id] = final_di
    event_id_comment_dict[ev_obj.id] = event_comments_list

  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)

    if valid_user:  
      user_going_events = UserGoingEvent.objects.filter(user_obj=user_obj)
      user_created_events = EventDetail.objects.filter(user_obj=user_obj)

      user_going_list = []
      user_created_events_list = []
      for ug_obj in user_going_events:
        user_going_list.append(ug_obj.event_obj.id)
      
      for uc_event in user_created_events:
        user_created_events_list.append(uc_event.id)

      return JsonResponse({
        'data': final_list, 
        'event_id_dict': [event_id_dict], 
        'event_id_comment_dict': [event_id_comment_dict],
        'user_event_going_list': [user_going_list],
        'user_created_event_list': [user_created_events_list]
      })

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except:
    return JsonResponse({
      'data': final_list, 
      'event_id_dict': [event_id_dict], 
      'event_id_comment_dict': [event_id_comment_dict],
      'user_event_going_list': [[]],
      'user_created_event_list': [[]]
    })



@csrf_exempt
@require_POST
def user_attending_event(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)
    
    if valid_user:
      event_id = json_data['event_id']
      event_objects = EventDetail.objects.filter(id=event_id)

      if len(event_objects) == 1:
        # verify this user is not already going to this event!
        uge_objects = UserGoingEvent.objects.filter(user_obj=user_obj, event_obj=event_objects[0])

        if len(uge_objects) == 0:
          uge = UserGoingEvent.objects.create(
            user_obj=user_obj,
            event_obj=event_objects[0]
          )
          uge.save()

          return JsonResponse({'success': True})

        else: 
          return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

      else: 
        return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})


@csrf_exempt
@require_POST
def unattend_event(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)

    if valid_user:
      event_id = json_data['event_id']
      event_objects = EventDetail.objects.filter(id=event_id)

      if len(event_objects) == 1:
        uge_obj = UserGoingEvent.objects.filter(
          user_obj=user_obj,
          event_obj=event_objects[0]
        )

        if len(uge_obj) == 1: 
          uge_obj[0].delete()
          return JsonResponse({'success': True})
        else: 
          return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

      else: 
        return JsonResponse({'success': False, 'reason': 'invalid data sent.'})
      
    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def delete_event(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)

    if valid_user:
      event_id = json_data['event_id']
      event_objects = EventDetail.objects.filter(id=event_id)

      if len(event_objects) == 1: 
        event_obj = event_objects[0]
        if event_obj.user_obj == user_obj:
          event_obj.delete()
          return JsonResponse({'success': True})

        else: 
          return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def create_comment(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)

    if valid_user:
       
      user_comment = json_data['comment']
      event_id = json_data['event_id']
      event_objects = EventDetail.objects.filter(id=event_id)
      if len(event_objects) == 1:
        event_obj = event_objects[0]

        ec = EventComments.objects.create(
          comment_text=user_comment,
          user_obj=user_obj,
          event_obj=event_obj
        )
        ec.save()

        user_who_created_event = event_obj.user_obj  # TODO: just notifying the person who created the event for now...
        notification_device_tokens = [user_who_created_event.phone_device_token]
        utils.send_user_notification(notification_device_tokens, type='create_comment')
        return JsonResponse({'success': True})

      else: 
        return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def get_user_profile_info(request):
  try:
    json_data = json.loads(request.body) 
    valid_user, user_obj = validate_user(json_data)
    
    if valid_user:
      user_profile_info = {
        'success': True,
        'data': {
          'name': user_obj.full_name,
          'user_profile_pic': user_obj.profile_picture_url,
        }
      }
      return JsonResponse(user_profile_info)

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except: 
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})



@csrf_exempt
@require_POST
def fetch_comments(request):
  try:
    json_data = json.loads(request.body)
    
    if 'event_id' in json_data:
      event_id = json_data['event_id']
      event_objects = EventDetail.objects.filter(id=event_id)

      if len(event_objects) == 1: 
        comments_objects = EventComments.objects.filter(event_obj=event_objects[0])

        event_comments_list = []
        for ec_obj in comments_objects:
          event_comments_list.append({
            'user_full_name': ec_obj.user_obj.full_name,
            'user_profile_pic': ec_obj.user_obj.profile_picture_url,
            'comment': ec_obj.comment_text
            })

        return JsonResponse({'success': True, 'data': event_comments_list})
      
      else: 
        return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except: 
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})









