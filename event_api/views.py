from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError

import requests
import json
from django.http import JsonResponse

from . import utils
from .models import UserProfile, EventDetail





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
    print('json-data:', json_data)
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

        user_google_id = user_data['sub']
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
        return JsonResponse({'success': False, 'reason': 'invalid token sent.'})
        
    else: 
      return JsonResponse({'success': False, 'reason': 'invalid token sent.'})

  except:
    return JsonResponse({'success': False, 'reason': 'invalid data sent.'})







