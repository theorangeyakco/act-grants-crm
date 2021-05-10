from rest_framework import serializers

from donations.models import Company


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = ['name', 'goal', 'logo', 'active', 'created_at']
