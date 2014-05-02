from django.test import TestCase
import datetime
from django.utils import timezone
from gist2.models import Gist
from django.core.urlresolvers import reverse

# Create your tests here.
class GistMethodTests(TestCase):
  def test_is_recent_with_future_poll(self):
    future_gist = Gist(pub_date=timezone.now() + datetime.timedelta(days=1))
    self.assertEqual(future_gist.is_recent(), False)

  def test_is_recent_with_old_gist(self):
    old_gist = Gist(pub_date=timezone.now() - datetime.timedelta(days=30))
    self.assertEqual(old_gist.is_recent(), False)

  def test_is_recent_with_recent_gist(self):
    recent_gist = Gist(pub_date=timezone.now() - datetime.timedelta(hours=1))
    self.assertEqual(recent_gist.is_recent(), True)

def create_gist(text, days):
 return Gist.objects.create(text=text,
     pub_date=timezone.now() + datetime.timedelta(days=days),user_id=1)

class GistViewTests(TestCase):
  def test_index_view_with_no_gists(self):
    response = self.client.get(reverse('index'))
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "There are no gists available")
    self.assertQuerysetEqual(response.context['latest_gists'], [])

  def test_index_view_with_a_past_gist(self):
    create_gist(text="Past gist", days=-30)
    response = self.client.get(reverse('index'))
    self.assertQuerysetEqual(
	response.context['latest_gists'],
	['<Gist: Past gist>']
    )

  def test_index_view_with_a_future_gist(self):
    create_gist(text="Future gist", days=+30)
    response = self.client.get(reverse('index'))
    self.assertContains(response, "There are no gists available", status_code = 200)
    self.assertQuerysetEqual(response.context['latest_gists'], [])

  def test_index_view_with_a_future_and_past_gists(self):
    create_gist(text="Future gist", days=+30)
    create_gist(text="Past gist", days=-30)
    response = self.client.get(reverse('index'))
    self.assertQuerysetEqual(
	response.context['latest_gists'],
	['<Gist: Past gist>']
    )

  def test_index_view_with_two_past_gists(self):
    create_gist(text="Past gist 1", days=-30)
    create_gist(text="Past gist 2", days=-31)
    response = self.client.get(reverse('index'))
    self.assertQuerysetEqual(
	response.context['latest_gists'],
	['<Gist: Past gist 1>','<Gist: Past gist 2>']
    )
