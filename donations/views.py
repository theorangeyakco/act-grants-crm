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
		data = request.POST
		print(request.data)
		payment = request.data['payload']['payment']['entity']
		donor = payment.get('notes')
		Donation.objects.create(rzp_payment_id=payment.get('id'), amount=int(payment.get('amount')),
		                        currency=payment.get('currency'), donor_name=donor.get('name'),
		                        donor_email=donor.get('email'), donor_pan=donor.get('pan'),
		                        donor_address=donor.get('address'), donor_country=donor.get('donor_country'),
		                        donor_zipcode=donor.get('zipcode'),
		                        payment_time=datetime.fromtimestamp(int(payment['payload']['payment']['entity']['created_at']), timezone.utc),
		                        rzp_response=request.data, domestic=True, international=False, success=payment.get('captured'))


		# client = razorpay.Client(auth=(os.getenv('RZP_KEY'), os.getenv("RZP_SECRET_KEY")))
		# try:
		# 	client.utility.verify_webhook_signature(request.data, webhook_signature, os.getenv('RZP_DOMESTIC_WEBHOOK_SECRET'))
		# except SignatureVerificationError:
		# 	return Response({'status': 'false', 'detail': 'Webhook signature verification error.'})
		return Response(200)