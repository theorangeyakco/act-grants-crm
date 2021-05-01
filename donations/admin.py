from django.contrib import admin

# Register your models here.

class DonationAdmin(admin.ModelAdmin):
	list_display =('amount', 'domestic', 'international', 'donor_email', 'donor_phone', 'payment_time')
	list_filter = ('domestic', 'international', 'payment_time', 'created_at')
	search_fields = ('donor_name', 'donor_email')
