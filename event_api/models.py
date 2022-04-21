from django.db import models



# "user": {"email": "duggalr42@gmail.com", "familyName": "Duggal", "givenName": "Rahul", "id": "115871519642305824560", "name": "Rahul Duggal", "photo": "https://lh3.googleusercontent.com/a/AATXAJwFjGR2J-5lAvvx633F9BwuA4W7kX1u0sbm-T65=s96-c"}
class UserProfile(models.Model):
  google_profile_id = models.CharField(max_length=1000)  
  first_name = models.CharField(max_length=1000)
  last_name = models.CharField(max_length=1000)
  full_name = models.CharField(max_length=1000)
  email = models.EmailField()  
  profile_picture_url = models.URLField()


class EventDetail(models.Model):
  event_title = models.CharField(max_length=1000)
  # activity_type = models.CharField(max_length=1000)
  park_name = models.CharField(max_length=1000)
  park_address = models.CharField(max_length=2000)
  event_description = models.TextField()
  timestamp_created = models.DateField(auto_now_add=True)
  event_date = models.DateField()
  event_time = models.TimeField()
  user_obj = models.ForeignKey(UserProfile, on_delete=models.CASCADE)





 