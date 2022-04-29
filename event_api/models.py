from pyexpat import model
from django.db import models


class UserProfile(models.Model):
  google_profile_id = models.CharField(max_length=1000)  
  first_name = models.CharField(max_length=1000)
  last_name = models.CharField(max_length=1000)
  full_name = models.CharField(max_length=1000)
  email = models.EmailField()  
  profile_picture_url = models.URLField()
  phone_device_token = models.CharField(max_length=1000, default='')


class EventDetail(models.Model):
  event_title = models.CharField(max_length=1000)
  # activity_type = models.CharField(max_length=1000)
  park_name = models.CharField(max_length=1000)
  park_address = models.CharField(max_length=2000, default='')
  event_description = models.TextField()
  timestamp_created = models.DateField(auto_now_add=True)
  event_date = models.DateField()
  event_time = models.TimeField()
  user_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class UserGoingEvent(models.Model):
  timestamp_created = models.DateField(auto_now_add=True)
  user_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  event_obj = models.ForeignKey(EventDetail, on_delete=models.CASCADE)


class EventComments(models.Model):
  timestamp_created = models.DateField(auto_now_add=True)
  comment_text = models.TextField()
  user_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  event_obj = models.ForeignKey(EventDetail, on_delete=models.CASCADE)







 