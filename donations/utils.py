import json
import os
from typing import Union

import requests

from donations.models import Company


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
		if json.loads(response.text)["error"] == "CONTACT_EXISTS":
			return
		raise Exception("Hubspot contact creation failed")

	return
