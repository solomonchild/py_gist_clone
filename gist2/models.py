from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User

# Create your models here.
class Gist(models.Model):
	text = models.TextField(null=False, blank=False)
	pub_date = models.DateTimeField('date published')
	user = models.ForeignKey(User)
	def __unicode__(self):
		return self.text
	def is_recent(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
	is_recent.short_description = "Is recent?"
