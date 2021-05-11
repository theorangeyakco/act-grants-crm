import json
import os
from datetime import datetime, timezone, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from razorpay.errors import SignatureVerificationError
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import razorpay
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError



from donations.models import Donation
from donations.serializers import DonationSerializer
from donations.utils import get_company_from_email


class AcceptWebhook(APIView):
	"""
	Accepts webhook from Razorpay and records the payment.
	Also performs any actions on payment recipt.
	"""

	@staticmethod
	def post(request):
		# client = razorpay.Client(auth=(os.getenv('RZP_KEY'), os.getenv("RZP_SECRET_KEY")))
		# try:
		# 	payload_body = json.dumps(request.data, separators=(',', ':'))
		# 	client.utility.verify_webhook_signature(payload_body, request.headers['X-Razorpay-Signature'],
		# 	                                        os.getenv('RZP_DOMESTIC_WEBHOOK_SECRET'))
		# except SignatureVerificationError:
		# 	return Response({'status': 'false', 'detail': 'Webhook signature verification error.'}, status=424)
		if request.data['event'] == 'payment.captured' or request.data['event'] == 'payment.failed':
			payment = request.data['payload']['payment']['entity']
			donor = payment.get('notes')
			Donation.objects.create(rzp_payment_id=payment.get('id'), amount=int(payment.get('amount')/100),
			                        currency=payment.get('currency'), donor_name=donor.get('name'),
			                        donor_email=donor.get('email_address'), donor_pan=donor.get('pan_number'),
			                        donor_address=donor.get('address'), donor_country="India",
			                        donor_zipcode=donor.get('zipcode'), donor_phone=donor.get('phone'),
			                        payment_time=datetime.fromtimestamp(int(request.data['payload']['payment']['entity']['created_at']), timezone.utc),
			                        rzp_response=request.data, domestic=True, international=False, success=payment.get('captured'),
			                        company=get_company_from_email(donor.get('email_address')))
		return Response(200)


class AcceptTestWebhook(APIView):
	"""
	Accepts webhook from Razorpay and records the payment.
	Also performs any actions on payment recipt.
	"""

	@staticmethod
	def post(request):
		print(request.data)
		print(request.headers)
		# client = razorpay.Client(auth=(os.getenv('RZP_KEY'), os.getenv("RZP_SECRET_KEY")))
		# try:
		# 	payload_body = json.dumps(request.data, separators=(',', ':'))
		# 	client.utility.verify_webhook_signature(payload_body, request.headers['X-Razorpay-Signature'],
		# 	                                        os.getenv('RZP_DOMESTIC_WEBHOOK_SECRET'))
		# except SignatureVerificationError:
		# 	return Response({'status': 'false', 'detail': 'Webhook signature verification error.'}, status=424)
		if request.data['event'] == 'payment.captured' or request.data['event'] == 'payment.failed':
			payment = request.data['payload']['payment']['entity']
			donor = payment.get('notes')
			Donation.objects.create(rzp_payment_id=payment.get('id'), amount=int(payment.get('amount')/100),
			                        currency=payment.get('currency'), donor_name=donor.get('name'),
			                        donor_email=donor.get('email_address'), donor_pan=donor.get('pan_number'),
			                        donor_address=donor.get('address'), donor_country="India",
			                        donor_zipcode=donor.get('zipcode'), donor_phone=donor.get('phone'),
			                        payment_time=datetime.fromtimestamp(int(request.data['payload']['payment']['entity']['created_at']), timezone.utc),
			                        rzp_response=request.data, domestic=True, international=False, success=payment.get('captured'),
			                        company=get_company_from_email(donor.get('email_address')))

			mailchimp = Client()
			mailchimp.set_config({
				"api_key": os.getenv('MAILCHIMP_API_KEY'),
				"server" : os.getenv('MAILCHIMP_DATA_CENTER'),
			})

			member_info = {
				"email_address": donor.get('email_address'),
				"status"       : "subscribed",
			}

			try:
				response = mailchimp.lists.add_list_member(os.getenv('MAILCHIMP_EMAIL_LIST_ID'), member_info)
			except Exception as error:
				print("An exception occurred: {}".format(error.text))

			html_message = render_to_string('donations/mails/test.html', {'name': donor.get('name')})
			email_subject = 'T'
			try:
				mailchimp = MailchimpTransactional.Client(os.getenv('MANDRILL_API_KEY'))
				response = mailchimp.messages.send({"message": {'html': html_message, 'subject': email_subject,
				                                             'from_email': 'admin@actgrants.in', 'from_name': 'ACT Grants',
				                                             'to': [{'email': donor.get('email_address'), 'name': donor.get('name')}],
				                                             'track_opens': True}})
				print(response)
			except ApiClientError as error:
				print("An exception occurred: {}".format(error.text))
		return Response(200)


class GetAllDonations(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		print(request.user)
		queryset = Donation.objects.filter(company=request.user.company)
		serializer = DonationSerializer(queryset, many=True)
		return Response(serializer.data, status=200)


class GetDonationStatistics(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		queryset = Donation.objects.filter(company=request.user.company)
		start_day = min(queryset.values_list('payment_time'))[0]
		end_day = max(queryset.values_list('payment_time'))[0] + timedelta(days=1)
		days = [start_day + timedelta(n)
		        for n in range(int((end_day - start_day).days))]
		values = []
		for date in days:
			s = queryset.filter(payment_time__day=date.day).aggregate(Sum('amount'))["amount__sum"]
			if s is None:
				values.append(0)
			else:
				values.append(s)
		stats = {'total': queryset.aggregate(Sum('amount')),
		         'daily': {'day': [days], 'values': [values]},
		         'count': queryset.aggregate(Count('amount'))}
		return Response(stats, status=200)
