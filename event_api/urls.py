from django.urls import path

from . import views


urlpatterns = [
  path('auth_signup', views.auth_signup, name='auth_signup'),

]


