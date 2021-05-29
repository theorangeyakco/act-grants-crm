from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views
from .views.statics import Index, Profile

urlpatterns = [
	path('', Index.as_view(), name='index'),
	path('accounts/profile/', Profile.as_view(), name='profile')
]
