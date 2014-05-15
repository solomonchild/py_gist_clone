from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden,  Http404 
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from gist2.models import Gist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

def index(request, page):
  template_name = "gists/index.html" 
  context_object_name = "latest_gists"
  gist_list = Gist.objects.all().order_by('-pub_date')
  paginator = Paginator(gist_list, 1)
  gists = paginator.page(page)
  params = {'latest_gists' : gists}
  return render(request, "gists/index.html", params)
	

@login_required
def detail_gist(request, gist_id):
  g = Gist.objects.get(pk=gist_id)
  params = {'gist':g}
  if not request.user.is_authenticated():
    return HttpResponseForbidden() 
  else:
    params['signed_in'] = True
  if 'error_message' in request.session:
    params['error_message'] = request.session['error_message']
    del request.session['error_message']
  return render(request, "gists/details.html", params)

@login_required
def edit_gist(request, gist_id):
  g = get_object_or_404(Gist, pk=gist_id)
  text = request.POST['text']
  if not text:
    url = reverse('detail_gist',args=(gist_id)) 
    request.session["error_message"] = "Shit"
    return HttpResponseRedirect(url)
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
