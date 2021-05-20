from datetime import timedelta

from django.db.models import Sum, Count
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet

from donations.models import Donation
from donations.serializers import DonationSerializer


class DonationFilter(FilterSet):
	class Meta:
		model = Donation
		fields = ['donor_name', 'donor_email', 'donor_phone', 'donor_country', 'currency', 'donor_zipcode', 'domestic',
		          'international']


class DonationViewSet(ReadOnlyModelViewSet, LimitOffsetPagination):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)
	filter_backends = (DjangoFilterBackend, SearchFilter)
	filterset_class = DonationFilter
	serializer_class = DonationSerializer
	search_fields = ('donor_name', 'donor_email', 'donor_phone', 'donor_country')

	def get_queryset(self):
		return Donation.objects.filter(company=self.get_serializer_context()['request'].user.company).order_by(
				'-created_at')


class GetDonationStatistics(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		queryset_domestic = Donation.objects.filter(company=request.user.company, domestic=True)
		end_day = max(queryset_domestic.values_list('payment_time'))[0] + timedelta(days=1)
		start_day = end_day - timedelta(days=7)
		days_domestic = [start_day + timedelta(n)
		                 for n in range(int((end_day - start_day).days))]
		values_domestic = []
		for date in days_domestic:
			s = queryset_domestic.filter(payment_time__day=date.day).aggregate(Sum('amount'))["amount__sum"]
			if s is None:
				values_domestic.append(0)
			else:
				values_domestic.append(s)

		queryset_international = Donation.objects.filter(company=request.user.company, international=True)
		end_day = max(queryset_international.values_list('payment_time'))[0] + timedelta(days=1)
		start_day = end_day - timedelta(days=7)
		days_international = [start_day + timedelta(n)
		                      for n in range(int((end_day - start_day).days))]
		values_international = []
		for date in days_international:
			s = queryset_international.filter(payment_time__day=date.day).aggregate(Sum('amount'))["amount__sum"]
			if s is None:
				values_international.append(0)
			else:
				values_international.append(s)
		stats = {'domestic'     : {'total': queryset_domestic.aggregate(Sum('amount')),
		                           'daily': {'day'   : [d.strftime("%d/%m/%y") for d in days_domestic],
		                                     'values': values_domestic},
		                           'count': queryset_domestic.aggregate(Count('amount'))},
		         'international': {'total': queryset_international.aggregate(Sum('amount')),
		                           'daily': {'day'   : [d.strftime("%d/%m/%y") for d in days_international],
		                                     'values': values_international},
		                           'count': queryset_international.aggregate(Count('amount'))}}

		return Response(stats, status=200)
