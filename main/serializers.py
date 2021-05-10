from donations.serializers import CompanySerializer
from main.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
	def __init__(self, *args, **kwargs):
		kwargs['partial'] = True
		super(UserSerializer, self).__init__(*args, **kwargs)

	company = CompanySerializer()

	class Meta:
		model = User
		fields = ['username', 'email', 'phone', 'avatar', 'name', 'first_name', 'last_name', 'company']

		extra_kwargs = {
			'username': {'read_only': True}
		}
