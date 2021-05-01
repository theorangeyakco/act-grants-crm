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
	donor_zipcode = models.CharField(max_length=16)
	payment_time = models.DateTimeField()
	rzp_response = JSONField()
	rzp_payment_id = models.CharField(max_length=32)
	currency = models.CharField(max_length=5)
	created_at = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f"Donation - {self.amount}"