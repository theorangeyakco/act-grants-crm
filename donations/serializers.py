from rest_framework import serializers

from donations.models import Company, Donation, SOURCE_CHOICES


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['name', 'goal', 'logo', 'active', 'created_at']


class DonationSerializer(serializers.ModelSerializer):
	class Meta:
		model = Donation
		fields = ['amount', 'domestic', 'international', 'source','donor_name',
		          'donor_email', 'donor_phone', 'donor_pan', 'donor_country',
		          'donor_address', 'donor_zipcode', 'payment_time', 'currency', 'meta']

	def to_representation(self, instance):
		data = super(DonationSerializer, self).to_representation(instance=instance)
		data['source'] = dict(SOURCE_CHOICES)[data['source']]
		return data
