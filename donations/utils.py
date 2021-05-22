import datetime
import json
import os
from typing import Union

import requests
import pandas as pd

from donations.models import Company, Donation


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
	print(response.text)
	if response.status_code >= 300:
		print(response.text)
		try:
			if json.loads(response.text)["error"] == "CONTACT_EXISTS":
				return
		except KeyError:
			if json.loads(response.text)["status"] == "error":
				raise Exception("Hubspot contact not created due to invalid email id")
		raise Exception("Hubspot contact creation failed")

	return

def get_company_from_code(code):
	return Company.objects.get(code=code)


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
		print('hi')
		date_list = df.iloc[i][3].split('/')
		date = datetime.datetime(int(date_list[2]), int(date_list[0]), int(date_list[1]))
		code = df.iloc[i][4]
		if not pd.isna(code):
			print(code)
			company = Company.objects.get(dr_code=code)
		else:
			company = None
		email = df.iloc[i][1]
		if pd.isna(email):
			email = None
		d = Donation(donor_name=df.iloc[i][0], donor_email=email, amount=int(df.iloc[i][2]),
		                          payment_time=date, company=company, international=True, domestic=False,
		                          currency='USD', source='dr', success=True)
		d.save()
		add_contact_to_hubspot(d.donor_name, '+11111', d.donor_email, 'Direct Relief', d.success)


