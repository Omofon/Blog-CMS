# a = "abc @gm ail. com "
# b = "abc@gmail.com "
# c = "abc=gmail.com"

# email_domain = ['gmail', 'yahoo', 'microsoft']

# x = b.split('@', 1)
# # if x in email_domain:
# #     print(True)
# # else:
# #     print(False)

# a_new = a.replace(' ', '')
# print(a_new)

# # if '@' not in a or ' ' in a:
# #     print("Invalid email")
# # else:
# #     print("good")

from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from passlib import pbkdf2_sha256

password = 'bcjs02ue0qh(02idh)'
# password_hash = make_password(password)
# print(password_hash)

django_hash = make_password(password)   
is_verified = django_pbkdf2_sha256.verify(password, django_hash)

if is_verified:
  print('Correct!!')

hash = pbkdf2_sha256.hash("password")
pbkdf2_sha256.verify("password", hash)


# <a href="/appname/detail/{{ job.id }}/">{{ job.name }}</a>
# <a href="{% url 'appname.views.detail' jobID=job.id %}">{{ job.name }}</a>

from django.conf import settings
from django.shortcuts import redirect


def my_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")