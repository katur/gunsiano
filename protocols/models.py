from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Protocol(models.Model):
    title_markdown = models.CharField('Title',
                                      max_length=250, unique=True,
                                      help_text=settings.MARKDOWN_PROMPT)
    title_url = models.CharField(max_length=250, unique=True)
    author = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        help_text='If none selected, will default to logged in user.')
    pub_date = models.DateField('Publication Date', auto_now=True)
    body_markdown = models.TextField('Body',
                                     help_text=settings.MARKDOWN_PROMPT)

    def __unicode__(self):
        return self.title_markdown

    def get_absolute_url(self):
        return reverse('protocol_url', args=[self.title_url])
