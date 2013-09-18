from django.db import models
from django.contrib.auth.models import User

class Protocol(models.Model):
	title = models.CharField('Title', max_length=250, unique=True)
	url_title = models.CharField(max_length=250, unique=True)
	author = models.ForeignKey(User, null=True, blank=True)
	pub_date = models.DateField('Publication Date', auto_now=True)
	body_markdown = models.TextField('Body', help_text='Use Markdown syntax.')
	def __unicode__(self):
		return self.title
