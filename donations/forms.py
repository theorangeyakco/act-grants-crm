from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError


class AddYPODonationForm(forms.Form):
	def __init__(self, *args, **kwargs):
		self.helper = FormHelper()
		self.helper.form_method = "POST"
		self.helper.add_input(Submit('submit', 'Add Donation', css_class='mt-1'))
		super(AddYPODonationForm, self).__init__(*args, **kwargs)

	amount = forms.IntegerField(label='Amount in INR')
	domestic = forms.BooleanField(required=False)
	international = forms.BooleanField(required=False)
	donor_name = forms.CharField()
	donor_email = forms.EmailField()
	donor_phone = forms.CharField()
	donor_pan_number = forms.CharField(label="PAN Number (enter N/A if not provided)")
	donor_address = forms.CharField()
	donor_country = forms.CharField()
	donor_zipcode = forms.CharField(label="Zip Code (enter N/A if not provided)")
	ypo_chapter_name = forms.CharField(label="YPO Chapter Name")
	ypo_member_reference_name = forms.CharField(label="YPO Member Reference (enter N/A if not provided)")
	ypo_region = forms.CharField(label="YPO Region (enter N/A if not provided)")

	def clean(self):
		cleaned_data = super().clean()
		domestic = cleaned_data.get('domestic')
		international = cleaned_data.get('international')

		if domestic and international:
			raise ValidationError("You can either choose domestic OR international")

		if (not domestic) and (not international):
			raise ValidationError("You must choose either domestic OR international")
