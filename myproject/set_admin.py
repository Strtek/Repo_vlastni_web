import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

try:
    admin_user = User.objects.get(email='trtekstanislav@gmail.com')
    admin_user.is_admin = True
    admin_user.save()
    print("Uživatel byl úspěšně aktualizován jako administrátor.")
except User.DoesNotExist:
    print("Uživatel s tímto e-mailem neexistuje.")