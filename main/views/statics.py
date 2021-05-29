from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class Index(View):
	@staticmethod
	def get(request):
		return render(request, 'global/index.html', {})


class Profile(LoginRequiredMixin, View):
	@staticmethod
	def get(request):
		if not request.user.is_staff:
			return HttpResponse(403)
		return render(request, 'main/profile.html', {})