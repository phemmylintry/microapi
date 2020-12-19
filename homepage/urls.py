from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('contact_us/', views.contact_us, name="contact"),
    path('faq/', views.faq, name="faq"),
    path('recover_password/',views.recover_password, name="recover_password"),
    path('reset_link/',views.reset_link, name="reset_link"),
    path('reset_password/',views.reset_password, name="reset_password"),
    path('blog/',views.blog_list, name="blog"),
    path('blog/post/',views.blog_post, name="blog_post"),
    path('blog/search/',views.blog_search, name="blog_search")
]
