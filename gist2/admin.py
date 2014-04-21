from django.contrib import admin
from gist2.models import Gist

# Register your models here.

class GistAdmin(admin.ModelAdmin):
	list_display = ('text', 'pub_date', 'is_recent')
	fieldsets =  [
		(None, {'fields':['text','user']}),
		('Date information', {'fields':['pub_date'], 'classes' :['collapse']})
	]
admin.site.register(Gist, GistAdmin)
