from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from donations.forms import AddYPODonationForm
from donations.models import Donation, Company


class AddYPODonationView(View):
	@staticmethod
	def get(request):
		form = AddYPODonationForm()
		return render(request, 'donations/manual/ypo.html', {
			'form': form
		})

	@staticmethod
	def post(request):
		form = AddYPODonationForm(request.POST)
		if form.is_valid():
			clean_data = form.cleaned_data
			donation = Donation(
					amount=clean_data['amount'],
					domestic=clean_data['domestic'],
					international=clean_data['international'],
					donor_name=clean_data['donor_name'],
					donor_email=clean_data['donor_email'],
					donor_phone=clean_data['donor_phone'],
					donor_pan=clean_data['donor_pan_number'],
					donor_address=clean_data['donor_address'],
					donor_country=clean_data['donor_country'],
					donor_zipcode=clean_data['donor_zipcode'],
					meta={"ypo_chapter_name"                                        : clean_data['ypo_chapter_name'],
					      "ypo_member_reference_name"                               : clean_data['ypo_member_reference_name'],
					      "i_agree_to_the_terms_and_conditions"                     : "Yes",
					      "donation_is_pursuant_to_section_135_of_the_companies_act": "Yes"},
					payment_time=timezone.now(),
					currency='INR',
					source='high_value',
					success=True,
					# company=Company.objects.get(slug="young_presidents_organization")
			)
			donation.save()
			messages.add_message(request, messages.SUCCESS, 'Donation added successfully.')
			return redirect(reverse('profile'))
		return render(request, 'donations/manual/ypo.html', {
			'form': form
		})
