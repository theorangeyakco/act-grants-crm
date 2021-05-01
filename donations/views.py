import json
import os
from datetime import datetime, timezone

from django.shortcuts import render

# Create your views here.
from razorpay.errors import SignatureVerificationError
from rest_framework.response import Response
from rest_framework.views import APIView
import razorpay

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