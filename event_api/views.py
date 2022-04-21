from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

import datetime
import requests
import json
from django.http import JsonResponse

from . import utils
from .models import UserProfile, EventDetail




park_address_info = {
  'Kipling Parkette': '7550 Kipling Avenue, Woodbridge, ON',
  'Smithfield Park': '173 Mt Olive Dr, Etobicoke, ON',
  'Waterfront Neighbourhood Centre': '627 Queens Quay W, Toronto, ON',
  'David Crombie Park Basketball Court': '115 Scadding Ave, Toronto, ON',
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




# TODO: obviously the csrf_exempt needs to be replaced
@csrf_exempt
@require_POST
def auth_signup(request):
  """
  save user profile info from Google 
    -validate user-idToken; if valid, get the associated data and save
  """
  try: 
    json_data = json.loads(request.body) 
    # print('json-data:', json_data)
    if 'idToken' in json_data:
      user_tok = json_data['idToken']
      valid, user_data = utils.new_google_validate_token(user_tok)
      if valid: 
        # (True, {
        #   'iss': 'https://accounts.google.com', 
        #   'azp': '770095547736-6g0e7nmfj72gki4pieu9v4d3si7p55m7.apps.googleusercontent.com', 
        #   'aud': '770095547736-7kq0ent6qtcpu1rf731bkvhmsc7cpg46.apps.googleusercontent.com', 
        #   'sub': '115871519642305824560', 
        #   'email': 'duggalr42@gmail.com', 
        #   'email_verified': True, 'name': 'Rahul Duggal', 
        #   'picture': 'https://lh3.googleusercontent.com/a/AATXAJwFjGR2J-5lAvvx633F9BwuA4W7kX1u0sbm-T65=s96-c', 
        #   'given_name': 'Rahul', 'family_name': 'Duggal', 'locale': 'en', 'iat': 1650476385, 'exp': 1650479985})

        # TODO: ensure google_profile_id not in DB already
        user_google_id = user_data['sub']
        user_objects = UserProfile.objects.filter(google_profile_id=user_google_id)
        if len(user_objects) == 0:
          user_email = user_data['email']
          user_full_name = user_data['name']
          user_profile_pic_url = user_data['picture']
          user_first_name = user_data['given_name']
          user_last_name = user_data['family_name']

          u = UserProfile.objects.create(
            google_profile_id=user_google_id,
            first_name=user_first_name,
            last_name=user_last_name,
            full_name=user_full_name,
            email=user_email,
            profile_picture_url=user_profile_pic_url
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
    print('json-event-form:', json_data)

#  {'event_title': 'Testing one', 'event_description': 'Sbbdjd xhxix', 'park_name': 'Indian Line Park', 'event_date': '2022-04-18T20:10:16.478Z', 'event_time': '6:00', 'access_token': 'ya29.A0ARrdaM-2hlXy4pxvCYIfCViQypx6g9N6QcaU0SW_eMAqNOc-o34rdoJhj2mVk7wViKsaijhH50eqhxNvojthDHBluj42GSue1AOuvDKoQ5s6ktmo_Jh_TjA5ZcZswSB9ac2p035IO1_3xseKSHWDcJ2lz09qdA'}
    if 'access_token' in json_data:
      user_access_token = json_data['access_token']
      access_token_res = utils.get_user_info(user_access_token)
      if 'error' not in access_token_res:
        # just assuming all the required fields in request
        user_profile_id = access_token_res['sub']
        user_objects = UserProfile.objects.filter(google_profile_id=user_profile_id)
        if len(user_objects) == 1: 
          event_title = json_data['event_title']
          event_desc = json_data['event_description']
          park_name = json_data['park_name']
          park_address = park_address_info[park_name]
          event_date = json_data['event_date'].split('T')[0]
          event_time = json_data['event_time']
          time_str_repres = time_mapping[event_time]
          time_dt_repres = datetime.datetime.strptime(time_str_repres, '%H:%M:%S').time()

          ed = EventDetail.objects.create(
            event_title = event_title,
            park_name = park_name,
            park_address = park_address,
            event_description = event_desc,
            event_date = event_date,
            event_time = time_dt_repres,
            user_obj = user_objects[0]
          )
          ed.save()

          return JsonResponse({'success': True})

        else: 
          return JsonResponse({'success': False, 'reason': 'invalid data sent.'})
        
      else:
        return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

    else: 
      return JsonResponse({'success': False, 'reason': 'invalid data sent.'})

  except: 
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})









