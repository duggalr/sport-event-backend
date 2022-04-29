import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
  def handle(self, *args, **options):
    if not User.objects.filter(username='rahul').exists():
      User.objects.create_superuser('rahul',
                                    'duggalr42@gmail.com',
                                    'Umakant12!')


