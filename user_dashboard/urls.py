from django.urls import path, re_path
from . import views

app_name = "user_dashboard"

urlpatterns = [
    path("main/", views.dash, name="dash_main"),
    path("main/<str:name>", views.oneproj, name="dash_proj"),
    path('create_api/', views.create_api, name='create_api'),
    path('', views.dash_rdrct, name='dashboardu'),
    re_path(r'^configure_api/(?P<proj_id>\d+)/(?P<api_id>\d+)$', views.configure_api, name='configure_api'),
    path("change/pass", views.change_password, name="change_pass"),
    
    re_path(r'^adding_api/(?P<proj_id>\d+)/(?P<id>\d+)$', views.adding_api, name='adding_api'),
    re_path(r'^activate/(?P<proj_id>\d+)/(?P<id>\d+)$', views.activate_api, name='activate_api'),
    # re_path(r'(?P<project_name>\w+)$', views.api_list, name='dashboard'),
    # re_path(r'(homepage/?P<name>\d+)$', views.home_page, name='home_page'),
    # re_path(r'^switch/(?P<id>\d+)$', views.switch, name='switch'),
    # re_path(r'^rmv_api/(?P<id>\d+)$', views.rmv_api, name='rmv_api'),
    
    path('logout/', views.logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('addProject/', views.addProject, name='addProject'),
    path('create_api_page/', views.create_api_page, name='create_api_page'),
    path('delete/<int:id>', views.delete_project, name='delete_project'),
    # re_path(r'^addProject/(?P<id>\d+)$', views.addProject, name='addProject'),
]