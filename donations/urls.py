from django.urls import path
from rest_framework.routers import DefaultRouter

from donations.views import AcceptWebhook


app_name = 'donations'

urlpatterns = [
	path('payment/new', AcceptWebhook.as_view(), name='accept_webhook'),
]
