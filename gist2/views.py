from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from gist2.models import Gist
from django.contrib.auth.models import User
from django.utils import timezone

# Create your views here.

class IndexView(generic.ListView):
  template_name = "gists/index.html" 
  context_object_name = "latest_gists"

  def get_queryset(self):
    return Gist.objects.filter(
      pub_date__lte=timezone.now()
      ).order_by('-pub_date')[:5]
	

class DetailGistView(generic.DetailView):
  model = Gist
  template_name = "gists/details.html"

def edit_gist(request, gist_id):
  g = get_object_or_404(Gist, pk=gist_id)
  text = request.POST['text']
  g.text = text
  g.save()
  return HttpResponseRedirect(reverse('index'))

class DetailUserView(generic.DetailView):
  model = User
  template_name = "users/details.html"

class UserGists(generic.ListView):
  template_name = "users/users_gists.html" 
  context_object_name = "user_gists"

  def get_queryset(self):
    return Gist.objects.order_by('-pub_date')[:5]
