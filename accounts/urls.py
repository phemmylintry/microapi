from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    # path('successCallback/', views.successCallback, name='successCallback'),
    # path('failureCallback/', views.failureCallback, name='failureCallback'),
    # path('oauth2callback/')
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    # path('oauth2callback/', views.oAuth2CallBackView, name="oauth2callback"),
    # path('recover/', views.pass_recovery, name='recover'),
    # path('logout', views.logout, name="logout"),
    # path('recover/sent', views.sent_link, name='sent-link'),
    # path("reset", views.reset_password, name="reset-password"),
    path('signout/', views.signout, name='signout')
]
