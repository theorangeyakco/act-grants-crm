from rest_framework import serializers

from donations.models import Company, Donation


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['name', 'goal', 'logo', 'active', 'created_at']


class DonationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Donation
		fields = ['amount', 'domestic', 'international', 'donor_name',
		          'donor_email', 'donor_phone', 'donor_pan', 'donor_country',
		          'donor_address', 'donor_zipcode', 'payment_time', 'currency']
