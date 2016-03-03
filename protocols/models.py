from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Protocol(models.Model):
    """
    An experimental protocol.
    """

    title = models.CharField(max_length=200,
                             help_text=settings.MARKDOWN_PROMPT)
    slug = models.SlugField(max_length=120, unique=True,
                            help_text="This is for the protocol's URL")
    author = models.ForeignKey(
        User, models.SET_NULL, null=True, blank=True,
        help_text='If none selected, defaults to logged in user')
    pub_date = models.DateField('Publication Date', auto_now=True)
    text = models.TextField(help_text=settings.MARKDOWN_PROMPT)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('protocol_url', args=[self.slug])
