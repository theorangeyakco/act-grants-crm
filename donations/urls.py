from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter

from donations.views.api import GetDonationStatistics, DonationViewSet
from donations.views.manual import AddYPODonationView
from donations.views.webhooks import AcceptInternationalWebhook, AcceptDomesticWebhook


app_name = 'donations'

donation_viewset_router = DefaultRouter()
donation_viewset_router.register(r'get_all_donations', DonationViewSet, basename='donation')

urlpatterns = [
	path('payment/new', csrf_exempt(AcceptDomesticWebhook.as_view()), name='accept_webhook'),
	path('payment_international/new', csrf_exempt(AcceptInternationalWebhook.as_view()), name='accept_webhook'),

	path('get_statistics/', GetDonationStatistics.as_view(), name='get_statistics'),

	path('add_donation/ypo/', AddYPODonationView.as_view(), name='add_ypo_donation')
]

urlpatterns += donation_viewset_router.urls