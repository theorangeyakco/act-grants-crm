from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

SOURCE_CHOICES = [('rzp_intl', 'Razorpay International'),
                  ('rzp_dom', 'Razorpay Domestic'),
                  ('dr', 'Direct Relief'),
                  ('high_value', 'High Value Donor')]


class Donation(models.Model):
	amount = models.IntegerField()
	domestic = models.BooleanField()
	international = models.BooleanField()
	success = models.BooleanField()
	donor_name = models.CharField(max_length=256)
	donor_email = models.EmailField(null=True)
	donor_phone = models.CharField(max_length=128, null=True)
	donor_pan = models.CharField(max_length=128, null=True, blank=True)
	donor_address = models.CharField(max_length=2048, null=True)
	donor_country = models.CharField(max_length=128, null=True)
	donor_zipcode = models.CharField(max_length=128, null=True, blank=True)
	payment_time = models.DateTimeField()
	meta = JSONField(null=True, blank=True)
	rzp_response = JSONField(null=True)
	rzp_payment_id = models.CharField(max_length=32, null=True, blank=True)
	source = models.CharField(max_length=16, choices=SOURCE_CHOICES)
	currency = models.CharField(max_length=5, choices=[('INR', 'INR'), ('USD', 'USD')])
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
