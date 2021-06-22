import time
from datetime import datetime
import decimal
import json
import os
from typing import Union

import requests
import pandas as pd

from donations.models import Company, Donation, SOURCE_CHOICES


def get_company_from_email(email: str):
	try:
		return Company.objects.get(domains__name=email.split('@')[-1])
	except Company.DoesNotExist:
		return None


def get_company_from_notes(notes: dict) -> Union[Company, None]:
	"""
	This function parses the notes dict from razorpay to get the
	company that, that payment is related to.

	notes = {..., 'organization': 'Lumen' ,...} -> Lumen
	notes = {..., 'organization': 'Google' ,...} -> Google
	notes = {..., 'company': 'Microsoft' ,...} -> Microsoft
	notes = {..., 'iilf_relationship_manager': '*', ...} -> IILF
	notes = {..., 'oyc': '*', ...} -> The Orange Yak Co.

	:param notes: dict from razorpay webhook response
	:return: Company object or None
    """

	for k in notes.keys():
		c = Company.objects.filter(rzp_identifier_key=k)
		if len(c) > 1:
			c = c.filter(rzp_identifier_value=notes[k])
			if len(c) > 1:
				print("Error: Key Value Pair is not Unique", c)
			return c[0]
		if len(c) == 1:
			return c[0]
	return None


def add_contact_to_hubspot(name: str, phone: str, email: str, act_donor_source: str, act_donated: bool):
	url = f"https://api.hubapi.com/contacts/v1/contact/?hapikey={os.environ.get('HUBSPOT_API_KEY')}"
	headers = {"Content-Type": "application/json"}
	payload = {
		"properties": [
			{"property": "firstname", "value": name.split()[0].strip()},
			{"property": "lastname", "value": name.strip().split()[-1]},
			{"property": "email", "value": email},
			{"property": "phone", "value": phone},
			{"property": "act_donor_source", "value": act_donor_source},
			{"property": "act_donated", "value": act_donated},
		]
	}
	response = requests.post(url=url, data=json.dumps(payload), headers=headers)
	if response.status_code >= 300:
		print(response.text)
		try:
			if json.loads(response.text)["error"] == "CONTACT_EXISTS":
				return
		except KeyError:
			if json.loads(response.text)["status"] == "error":
				print("Hubspot contact not created due to invalid email id")
			print("Hubspot contact creation failed")

	return


def num2words(num):
	num = decimal.Decimal(num)
	decimal_part = num - int(num)
	num = int(num)

	if decimal_part:
		return num2words(num) + " point " + (" ".join(num2words(i) for i in str(decimal_part)[2:]))

	under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Eleven',
	            'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen', 'Nineteen']
	tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
	above_100 = {100: 'Hundred', 1000: 'Thousand', 100000: 'Lakhs', 10000000: 'Crores'}

	if num < 20:
		return under_20[num]

	if num < 100:
		return tens[num // 10 - 2] + ('' if num % 10 == 0 else ' ' + under_20[num % 10])

	# find the appropriate pivot - 'Million' in 3,603,550, or 'Thousand' in 603,550
	pivot = max([key for key in above_100.keys() if key <= num])

	return num2words(num // pivot) + ' ' + above_100[pivot] + ('' if num % pivot == 0 else ' ' + num2words(num % pivot))


def send_80g_receipt(name: str, address: str, email: str, date: datetime, pan_number: str, rzp_id: str,
                     amount: int):
	url = f"https://api.hubapi.com/email/public/v1/singleEmail/send?hapikey={os.environ.get('HUBSPOT_API_KEY')}"
	headers = {"Content-Type": "application/json"}
	payload = {
		"emailId"         : 49207934017,
		"message"         : {
			"to"    : email.lower(),
			"cc"    : ["actgrants.developers@gmail.com"],
			"sendId": rzp_id,
		},
		"customProperties": [
			{
				"name" : "receipt_date",
				"value": date.strftime("%d/%m/%Y")
			},
			{
				"name" : "address",
				"value": address.lower().capitalize()
			},
			{
				"name" : "pan_number",
				"value": pan_number.upper(),
			},
			{
				"name" : "name",
				"value": name.lower().capitalize()
			},
			{
				"name" : "rzp_id",
				"value": rzp_id.lower()
			},
			{
				"name" : "receipt_no",
				"value": "ACT/" + rzp_id[4:].lower() + f"/{date.strftime('%D%M%Y')}"
			},
			{
				"name" : "total_donation_amount",
				"value": amount,
			},
			{
				"name" : "total_donation_amount_in_words",
				"value": num2words(amount)
			},
		]
	}
	response = requests.post(url=url, data=json.dumps(payload), headers=headers)
	print(response.text)
	if response.status_code >= 300:
		pass
	return


def send_80g_from_excel(path):
	df = pd.read_csv(path, sep=",")
	for i in range(0, len(df)):
		date = datetime.strptime(df.iloc[i][0], "%d/%m/%Y %I:%M:%S")
		amount = int(df.iloc[i][1])
		rzp_id = df.iloc[i][2]
		name = df.iloc[i][3]
		email = df.iloc[i][5]
		pan = df.iloc[i][6]
		address = df.iloc[i][7]
		send_80g_receipt(name, address, email, date, pan, rzp_id, amount)
		time.sleep(1)


def pop_country_from_notes(notes):
	try:
		return notes.pop('country').lower().strip()
	except KeyError:
		return notes.pop('nationality_or_domicile').lower().strip()


def pop_name_from_notes(notes):
	if notes.get('name', False):
		return notes.pop('name').title()
	if notes.get('donor_name_or_company_name', False):
		return notes.pop('donor_name_or_company_name').title()
	if notes.get('donor_name', False):
		return notes.pop('donor_name').title()


def add_donations_from_dr(path):
	"""
	This function adds donations from an excel file of the following
	format:
	Name | Email | Amount | Date | Code

	Name -> Full Donor Name
	Email -> Valid email address
	Amount -> Float/Int in USD
	Date -> mm/dd/yy
	Code -> String code
	:param path: path to donations file
	:return:
	"""
	df = pd.read_csv(path, sep=',')
	for i in range(1, len(df)):
		date_list = df.iloc[i][3].split('/')
		date = datetime.datetime(int(date_list[2]), int(date_list[0]), int(date_list[1]))
		code = df.iloc[i][4]
		if not pd.isna(code):
			print(code)
			try:
				company = Company.objects.get(dr_code=code)
			except Company.DoesNotExist:
				company = None
		else:
			company = None
		email = df.iloc[i][1]
		if pd.isna(email):
			email = None
		d = Donation(donor_name=df.iloc[i][0], donor_email=email, amount=int(df.iloc[i][2]),
		             payment_time=date, company=company, international=True, domestic=False,
		             currency='USD', source='dr', success=True, country='USA', donor_phone='-')
		d.save()
		add_contact_to_hubspot(d.donor_name, '+11111', d.donor_email, 'Direct Relief', d.success)


def normalize_source(raw_src):
	return dict(SOURCE_CHOICES)[raw_src]
