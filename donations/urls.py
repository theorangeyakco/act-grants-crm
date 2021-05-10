from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from donations.views import AcceptWebhook, AcceptTestWebhook, GetDonationStatistics, GetAllDonations


app_name = 'donations'

urlpatterns = [
	path('payment/new', csrf_exempt(AcceptWebhook.as_view()), name='accept_webhook'),
	path('payment_test/new', csrf_exempt(AcceptTestWebhook.as_view()), name='accept_webhook'),

	path('get_all_donations/', GetAllDonations.as_view(), name='get_donations'),
	path('get_statistics/', GetDonationStatistics.as_view(), name='get_statistics')
]
