from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from donations.views.api import GetAllDonations, GetDonationStatistics
from donations.views.webhooks import AcceptInternationalWebhook, AcceptDomesticWebhook


app_name = 'donations'

urlpatterns = [
	path('payment/new', csrf_exempt(AcceptDomesticWebhook.as_view()), name='accept_webhook'),
	path('payment_international/new', csrf_exempt(AcceptInternationalWebhook.as_view()), name='accept_webhook'),

	path('get_all_donations/', GetAllDonations.as_view(), name='get_donations'),
	path('get_statistics/', GetDonationStatistics.as_view(), name='get_statistics')
]
