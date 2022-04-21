from django.urls import path

from . import views


urlpatterns = [
  path('auth_signup', views.auth_signup, name='auth_signup'),
  path('get_events', views.get_events, name='get_events'),
  path('create_event', views.create_event, name='create_event'),

]

