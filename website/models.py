from django.db import models
from django.contrib.auth.models import User

class Position(models.Model):
	position = models.CharField(max_length=50)
	display_order = models.PositiveSmallIntegerField(unique=True)
	def __unicode__(self):
		return self.position
	class Meta:
		ordering = ["display_order"]

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	position = models.ForeignKey(Position)
	in_abu_dhabi = models.NullBooleanField(null=True)
	is_current = models.BooleanField(default=True)
	net_id = models.CharField(max_length=25, blank=True)
	url = models.URLField(blank=True)
	blurb = models.TextField('Blurb',
		help_text='''Use Markdown syntax.
			See
			<a href="http://www.darkcoding.net/software/markdown-quick-reference" target="_blank">
			a quick reference</a>,
			<a href="http://www.markdowntutorial.com/" target="_blank">a tutorial</a>,
			or practice <a href="http://dillinger.io/" target="_blank">here</a>.''',
		blank=True
	)
	image_filename = models.CharField(max_length=100, blank=True)
	def __unicode__(self):
		return self.user.get_full_name()
	class Meta:
		ordering = ["net_id"]

class ResearchArea(models.Model):
	name = models.CharField(max_length=60, unique=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	filename = models.CharField(max_length=50, unique=True, blank=True)
	filename_is_video = models.BooleanField(default=False)
	description = models.TextField('Description',
		help_text='''Use Markdown syntax.
			See
			<a href="http://www.darkcoding.net/software/markdown-quick-reference" target="_blank">
			a quick reference</a>,
			<a href="http://www.markdowntutorial.com/" target="_blank">a tutorial</a>,
			or practice <a href="http://dillinger.io/" target="_blank">here</a>.''',
	)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ["display_order"]

class Resource(models.Model):
	name = models.CharField(max_length=40, unique=True)
	display_order = models.PositiveSmallIntegerField(unique=True)
	logo_filename = models.CharField(max_length=50, blank=True)
	url = models.CharField(max_length=100, blank=True)
	description = models.TextField('Description',
		help_text='''Use Markdown syntax.
			See
			<a href="http://www.darkcoding.net/software/markdown-quick-reference" target="_blank">
			a quick reference</a>,
			<a href="http://www.markdowntutorial.com/" target="_blank">a tutorial</a>,
			or practice <a href="http://dillinger.io/" target="_blank">here</a>.''',
	)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ["display_order"]
