from django.urls import path
from . import views


urlpatterns = [
    # path('api/', views.api_view)
    path('docs/<slug:slug>', views.docs, name="docs"),
]