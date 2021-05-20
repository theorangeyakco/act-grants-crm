from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField


class Donation(models.Model):
	amount = models.IntegerField()
	domestic = models.BooleanField()
	international = models.BooleanField()
	success = models.BooleanField()
	donor_name = models.CharField(max_length=256)
	donor_email = models.EmailField()
	donor_phone = models.CharField(max_length=16)
	donor_pan = models.CharField(max_length=16, null=True, blank=True)
	donor_address = models.CharField(max_length=2048)
	donor_country = models.CharField(max_length=32)
	donor_zipcode = models.CharField(max_length=16, null=True, blank=True)
	payment_time = models.DateTimeField()
	meta = JSONField(null=True)
	rzp_response = JSONField()
	rzp_payment_id = models.CharField(max_length=32)
	currency = models.CharField(max_length=5)
	company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Donation - {self.amount}"


class Company(models.Model):
	class Meta:
		verbose_name_plural = 'Companies'
		unique_together = [('rzp_identifier_key', 'rzp_identifier_value')]

	name = models.CharField(max_length=128)
	slug = models.SlugField(max_length=128)
	logo = models.URLField(null=True)
	goal = models.IntegerField()
	active = models.BooleanField(default=True)
	dr_code = models.CharField(max_length=10)
	rzp_identifier_key = models.CharField(max_length=128)
	rzp_identifier_value = models.CharField(max_length=128, null=True)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Company - {self.name}"

class Domain(models.Model):
	name = models.CharField(max_length=128)

	def __str__(self):
		return f"{self.name}"
