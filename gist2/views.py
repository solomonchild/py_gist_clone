from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from gist2.models import Gist

# Create your views here.

def index(request):
	latest_gists = Gist.objects.order_by('-pub_date')[:5]
	context = {'latest_gists' : latest_gists, }
	return render(request, 'gists/index.html', context)
	

def details_gist(request, gist_id):
	return HttpResponse("You are looking at gist %s" % gist_id)

def details_user(requests, user_id):
	return HttpResponse("You are looking at the profile %s" % user_id)

def user_gists(request, user_id):
	return HttpResponse("You are looking at gists of user %s" % user_id)
