import json
import os
from datetime import datetime, timezone

from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from razorpay.errors import SignatureVerificationError
from rest_framework.response import Response
from rest_framework.views import APIView
import razorpay
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError



from donations.models import Donation


class AcceptWebhook(APIView):
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
			                        rzp_response=request.data, domestic=True, international=False, success=payment.get('captured'))
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
			                        rzp_response=request.data, domestic=True, international=False, success=payment.get('captured'))

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
			email_subject = 'Test Subject'
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
