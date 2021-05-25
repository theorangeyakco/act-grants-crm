from datetime import datetime

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from donations.models import Donation
from donations.utils import get_company_from_notes, add_contact_to_hubspot, pop_country_from_notes, pop_name_from_notes


class AcceptDomesticWebhook(APIView):
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
			try:
				Donation.objects.get(rzp_payment_id=payment.get('id'))
			except Donation.DoesNotExist:
				notes = payment.get('notes')
				d = Donation(
						rzp_payment_id=payment.get('id'),
						amount=int(payment.get('amount') / 100),
						currency=payment.get('currency'),
						donor_name=pop_name_from_notes(notes),
						donor_email=notes.pop('email_address').lower(),
						donor_pan=notes.pop('pan_number').upper(),
						donor_address=notes.pop('address'),
						donor_phone=notes.pop('phone'),
						donor_country="India",
						payment_time=datetime.fromtimestamp(int(request.data['payload']['payment']['entity']['created_at']),
						                                    timezone.utc),
						rzp_response=request.data, domestic=True, international=False,
						source='rzp_dom',
						success=payment.get('captured'),
						company=get_company_from_notes(notes),
						meta=notes
				)
				d.save()
				add_contact_to_hubspot(d.donor_name, d.donor_phone, d.donor_email, 'Razorpay International', d.success)

		return Response(200)


class AcceptInternationalWebhook(APIView):
	"""Accepts webhook from Razorpay international and records the
	payment. Also adds contact to hubspot. """

	@staticmethod
	def post(request):
		if request.data['event'] == 'payment.captured' or request.data['event'] == 'payment.failed':
			payment = request.data['payload']['payment']['entity']
			try:
				Donation.objects.get(rzp_payment_id=payment.get('id'))
			except Donation.DoesNotExist:
				notes = payment.get('notes')
				d = Donation(
						rzp_payment_id=payment.get('id'),
	                    amount=int(payment.get('amount') / 100),
						currency=payment.get('currency'),
						donor_name=pop_name_from_notes(notes),
						donor_email=notes.pop('email_address').lower(),
						donor_address=notes.pop('address'),
						donor_phone=notes.pop('phone'),
						donor_country=pop_country_from_notes(notes),
						donor_zipcode=notes.pop('zipcode').upper().strip(),
						payment_time=datetime.fromtimestamp(int(request.data['payload']['payment']['entity']['created_at']),
						                                    timezone.utc),
						success=payment.get('captured'),
						company=get_company_from_notes(notes),
						meta=notes,
						domestic=False,
						international=True,
						source='rzp_intl',
						rzp_response=request.data
				)
				d.save()
				add_contact_to_hubspot(d.donor_name, d.donor_phone, d.donor_email, 'Razorpay International', d.success)

		return Response()