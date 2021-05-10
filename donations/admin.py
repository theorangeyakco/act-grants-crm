from django.contrib import admin

# Register your models here.
from donations.models import Donation, Company, Domain


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
	list_display =('id', 'amount', 'success', 'domestic', 'international', 'donor_email', 'donor_phone', 'payment_time', 'company')
	list_filter = ('domestic', 'international', 'payment_time', 'created_at', 'company')
	search_fields = ('donor_name', 'donor_email')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
	list_display = ('name',)
	filter_horizontal = ('domains',)

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
	list_display = ('name',)
