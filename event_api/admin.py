from django.contrib import admin
from .models import UserProfile, EventDetail, UserGoingEvent, EventComments


admin.site.register(UserProfile)
admin.site.register(EventDetail)
admin.site.register(UserGoingEvent)
admin.site.register(EventComments)



