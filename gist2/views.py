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
from django.db import IntegrityError

# Create your views here.

def index(request, page=1):
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
  if 'success' in request.session:
    del request.session['success']
    params['success'] = 'true'
  return render(request, "gists/index.html", params)

def register(request):
  if request.method == "POST":
    errors=[]
    params={}
    if "username" not in request.POST or request.POST["username"] == "":
      errors.append('Username field is required')
    if "password1" not in request.POST or request.POST["password1"] == "":
      errors.append('Password is required')
    if "password2" not in request.POST or request.POST["password2"] == "":
      errors.append('Please confirm password')
    if "email" not in request.POST or request.POST["email"] == "":
      errors.append('Email field is required')
    if "password2" in request.POST and "password1" in request.POST and request.POST["password1"] != request.POST["password2"]:
      errors.append('Passwords do not match')
    params['errors']=errors
    if len(errors) != 0:
      return render(request, "registration/register.html", params)
    u = User(username=request.POST["username"], password=request.POST["password1"], email=request.POST["email"])
    try:
      u.save()
    except IntegrityError:
      errors.append("User with such username already exists")
      params['errors'] = errors
      return render(request, "registration/register.html", params)
    request.session['success'] = 'true'
    return HttpResponseRedirect(reverse('index'))
  else:
    return render(request, "registration/register.html")

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
def update_user(request, user_id):
  errors = []
  params = {}
  u = get_object_or_404(User, pk=user_id)
  if "fistname" in request.POST:
    u.first_name = request.POST['firstname']
  if "lastname" in request.POST:
    u.last_name = request.POST['lastname']
  if "password1" in request.POST and "password2" in request.POST and request.POST['password1'] != '' and request.POST['password1'] != request.POST['password2']:
    errors.append('Passwords should match')
  else:
    u.password = request.POST['password1']
  if "email" not in request.POST or request.POST["email"] == "":
    errors.append('Email field is required')
  else:
    u.email = request.POST['email']
  if len(errors) != 0:
    request.session["errors"] = errors
    return HttpResponseRedirect(reverse('detail_user', kwargs={'user_id':user_id}))
  try:
    u.save()
  except IntegrityError:
    errors.append("Problem with database")
    params['errors'] = errors
    return render(request, "users/details.html", params)
  request.session["success"] = ''
  return HttpResponseRedirect(reverse('detail_user', kwargs={'user_id':user_id}))

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
  paginator = Paginator(gists, 1)
  try:
    gists = paginator.page(page)
  except PageNotAnInteger:
    gists = paginator.page(1)
  except EmptyPage:
    gists = paginator.page(1)
  request.session["page"] = page
  params = {'user' :u, 'gists':gists}
  if 'errors' in  request.session:
    params['errors'] = request.session['errors']
    del request.session['errors']
  request.session["gobackto"] = request.path 
  return render(request, "users/details.html", params)
  

@login_required
class UserGists(generic.ListView):
  template_name = "users/users_gists.html" 
  context_object_name = "user_gists"

  def get_queryset(self):
    return Gist.objects.order_by('-pub_date')[:5]
