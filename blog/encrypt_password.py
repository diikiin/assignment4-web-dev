import os

from django.contrib.auth.hashers import make_password

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assignment4.settings")
password = "admin"
hashed_password = make_password(password)

print("Hashed Password:", hashed_password)
