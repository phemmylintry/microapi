# from django.contrib.auth.backends import BaseBackend, ModelBackend
# from django.contrib.auth import get_user_model
# from django.conf import settings
# import requests
# from .models import User
# from django.contrib import messages
# from django.core.exceptions import ValidationError


# HEADERS = {
#     "Authorization": "Bearer %s" % (settings.AUTH_ADMIN_TOKEN)
# }

# # class MyModelBack(ModelBackend):
# #     #def __init__(self, username, password)
# #     def authenticate(self, request, **kwargs):


# class ApiAuthBackend(BaseBackend):
#     """
#     Authenticate User against the email auth
#     """

#     def authenticate(self, request, **kwargs):
#         try:
#             if request.POST.get('next') == '/admin/' and request.POST.get('username'):
#                 username = request.POST.get('username')
#                 password = request.POST.get('password')
#                 try:
#                     user = get_user_model().objects.get(username=username)
#                     if user.is_superuser:
#                         user.username = username
#                         user.save()
#                         return user
#                 except get_user_model().DoesNotExist:
#                     return None
#         except:
#             pass

#         email = kwargs['email']
#         password = kwargs['password']

#         if email and password:
#             try:
#                 #endpoint = '{api_url}user/login'
#                 url = settings.AUTH_API_URL + 'user/login'

#                 payload = {
#                     "password": password,
#                     "email": email,
#                 }

#                 # response = requests.get(url, headers=headers, data = payload)
#                 response = requests.request(
#                     "POST", url, headers=HEADERS, data=payload)

#                 print(response)

#                 response = response.json()
#                 # data = response
#                 if response['success'] == True:
#                     user = get_user_model().objects.get(email=email)
#                     print(user)
#                     return user
#                 elif (response['data']['statusCode'] == 401 or response['data']['statusCode'] == 400):
#                     msg = 'Please verify your email to proceed'
#                     return None
#                 elif response['success'] == False:
#                     return None

 
#             except get_user_model().DoesNotExist:
#                 return None


#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except get_user_model().DoesNotExist:
#             return None