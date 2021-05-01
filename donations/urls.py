from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from donations.views import AcceptWebhook, AcceptTestWebhook


app_name = 'donations'

urlpatterns = [
	path('payment/new', csrf_exempt(AcceptWebhook.as_view()), name='accept_webhook'),
	path('payment_test/new', csrf_exempt(AcceptTestWebhook.as_view()), name='accept_webhook'),
]
