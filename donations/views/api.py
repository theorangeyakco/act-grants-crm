from datetime import timedelta

from django.db.models import Sum, Count
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from donations.models import Donation
from donations.serializers import DonationSerializer


class GetAllDonations(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		print(request.user)
		queryset = Donation.objects.filter(company=request.user.company)
		serializer = DonationSerializer(queryset, many=True)
		return Response(serializer.data, status=200)


class GetDonationStatistics(APIView):
	permission_classes = (IsAuthenticated,)
	authentication_classes = (TokenAuthentication,)

	@staticmethod
	def get(request):
		queryset = Donation.objects.filter(company=request.user.company)
		end_day = max(queryset.values_list('payment_time'))[0] + timedelta(days=1)
		start_day = end_day - timedelta(days=7)
		days = [start_day + timedelta(n)
		        for n in range(int((end_day - start_day).days))]
		values = []
		for date in days:
			s = queryset.filter(payment_time__day=date.day).aggregate(Sum('amount'))["amount__sum"]
			if s is None:
				values.append(0)
			else:
				values.append(s)
		stats = {'total': queryset.aggregate(Sum('amount')),
		         'daily': {'day': [d.strftime("%d/%m/%y") for d in days], 'values': values},
		         'count': queryset.aggregate(Count('amount'))}
		return Response(stats, status=200)
