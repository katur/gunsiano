from django.db import models
from website.models import UserProfile
import datetime

class Protocol(models.Model):
	title = models.CharField(max_length=250)
	url_title = models.CharField(max_length=100)
	author = models.ForeignKey(UserProfile, null=True)
	pub_date = models.DateTimeField(auto_now_add=True)
	body_markdown = models.TextField(help_text='Use Markdown syntax.')
	body = models.TextField(blank=True, null=True)

	class Admin:
		fields = (
			(None, {'fields': ('title', 'pub_date', 'body_markdown')}),
		)

	def save(self):
		import markdown
		self.body = markdown.markdown(self.body_markdown)
		super(Protocol, self).save() # Call the "real" save() method.
