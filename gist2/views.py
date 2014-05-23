from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden,  Http404 
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views import generic
from gist2.models import Gist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST

# Create your views here.

def index(request, page):
  gist_list = Gist.objects.all().order_by('-pub_date')
  paginator = Paginator(gist_list, 1)
  try:
    gists = paginator.page(page)
  except PageNotAnInteger:
    gists = paginator.page(1)
  except EmptyPage:
    gists = paginator.page(1)
  params = {'latest_gists' : gists}
  request.session["page"] = page
  request.session["gobackto"] = request.path 
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
@require_POST
def remove_user(request, user_id):
  u = get_object_or_404(User, pk=user_id)
  u.delete()
  if "gobackto" in request.session:
    temp = request.session["gobackto"]
    del request.session["gobackto"]
    return HttpResponseRedirect(temp)
  else:
    return HttpResponseRedirect(reverse('index', kwargs={'page' : p}))

@login_required
@require_POST
def remove_gist(request, gist_id):
  g = get_object_or_404(Gist, pk=gist_id)
  g.delete()
  if "gobackto" in request.session:
    temp = request.session["gobackto"]
    del request.session["gobackto"]
    return HttpResponseRedirect(temp)
  else:
    return HttpResponseRedirect(reverse('index', kwargs={'page' : p}))

@login_required
@require_POST
def edit_gist(request, gist_id):
  g = get_object_or_404(Gist, pk=gist_id)
  text = request.POST['text']
  print request.path
  if not text:
    url = reverse('detail_gist',args=(gist_id)) 
    request.session["error_message"] = "Shit"
    return HttpResponseRedirect(url)
  g.text = text
  g.save()
  p = 1;
  if "page" in request.session:
   p = request.session["page"] 
  return HttpResponseRedirect(reverse('index', kwargs={'page' : p}))


@login_required
def detail_user(request, user_id, page=1):
  u = get_object_or_404(User, pk=user_id)
  gists = Gist.objects.filter(user=user_id)
  params = {'latest_gists' : gists}
  paginator = Paginator(gists, 1)
  try:
    gists = paginator.page(page)
  except PageNotAnInteger:
    gists = paginator.page(1)
  except EmptyPage:
    gists = paginator.page(1)
  request.session["page"] = page
  params = {'user' :u, 'gists':gists}
  request.session["gobackto"] = request.path 
  return render(request, "users/details.html", params)
  

@login_required
class UserGists(generic.ListView):
  template_name = "users/users_gists.html" 
  context_object_name = "user_gists"

  def get_queryset(self):
    return Gist.objects.order_by('-pub_date')[:5]
