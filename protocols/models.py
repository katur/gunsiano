from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Protocol(models.Model):
  title_markdown = models.CharField(
      'Title', help_text=settings.MARKDOWN_PROMPT, max_length=250,
      unique=True)
  title_url = models.CharField(max_length=250, unique=True)
  author = models.ForeignKey(User, null=True, blank=True)
  pub_date = models.DateField('Publication Date', auto_now=True)
  body_markdown = models.TextField('Body', help_text=settings.MARKDOWN_PROMPT)

  def __unicode__(self):
    return self.title_markdown
