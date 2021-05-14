from typing import Union
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
