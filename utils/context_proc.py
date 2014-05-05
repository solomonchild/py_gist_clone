def is_authenticated(request):
  return {
      'signed_in' : request.user.is_authenticated(),
  }
