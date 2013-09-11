from django.db import models
from website.models import UserProfile
import datetime

class Protocol(models.Model):
	title = models.CharField('Title', max_length=250)
	url_title = models.CharField('URL Title (no spaces)', max_length=100)
	author = models.ForeignKey(UserProfile, null=True)
	pub_date = models.DateField(auto_now=True)
	body_markdown = models.TextField('Body', help_text='Use Markdown syntax.')
	def __unicode__(self):
		return self.title
