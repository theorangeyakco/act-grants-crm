from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from backend.media_storages import PrivateMediaStorage

class UserData(models.Model):
	NOTIFICATION_LEVEL_CHOICES = [
		(0, 'Disable All Notifications'),
		(1, 'Email me only when its critical'),
		(2, 'Email me reminders and updates'),
		(3, 'Email me some promotions'),
		(4, 'Keep all notifications on')
	]

	class Meta:
		abstract = True

	email = models.EmailField('Email Address', max_length=255)
	name = models.CharField('Full Name', max_length=128)
	phone = PhoneNumberField(null=True, blank=True)
	avatar = models.ImageField(storage=PrivateMediaStorage(),
	                           upload_to='user_data/avatars',
	                           null=True, blank=True)
	company = models.ForeignKey('donations.Company', on_delete=models.CASCADE, null=True)

	# setting 5 levels of notifications <0 - 4>
	# 0 is disabled to 4 is all notifications
	notification_level = models.IntegerField('Notification Level', default='4',
	                                         choices=NOTIFICATION_LEVEL_CHOICES)

	@property
	def first_name(self):
		try:
			return self.name.split()[0]
		except IndexError:
			return ''

	@property
	def last_name(self):
		try:
			return self.name.split()[-1]
		except IndexError:
			return ''


class AttemptData(models.Model):
	class Meta:
		abstract = True

	attempt_id = models.AutoField('Attempt ID', primary_key=True)
	username = models.CharField('Username', max_length=64)

	timestamp = models.DateTimeField('Timestamp', default=timezone.now)
	successful = models.BooleanField('Successful', default=0)
	ip_address = models.GenericIPAddressField(
			'IP Address', null=True, blank=True
	)

	def __str__(self):
		return f'{self.username} @ {self.timestamp}'
