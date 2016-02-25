import markdown
from markdown.inlinepatterns import SimpleTagPattern

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


SUBSCRIPT_RE = r'(\~)([^\~]*)\2'  # e.g. ~2~
SUPERSCRIPT_RE = r'(\^)([^\^]*)\2'  # e.g. ^2^


class SubscriptExtension(markdown.Extension):
    """ Subscript Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace subscript with SubscriptPattern """
        md.inlinePatterns.add('subscript',
                              SimpleTagPattern(SUBSCRIPT_RE, 'sub'),
                              '<not_strong')


class SuperscriptExtension(markdown.Extension):
    """ Superscript Extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Replace superscript with SuperscriptPattern """
        md.inlinePatterns.add('superscript',
                              SimpleTagPattern(SUPERSCRIPT_RE, 'sup'),
                              '<not_strong')


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def enhanced_markdown(value):
    extensions = [
        'nl2br',  # more intuitive linebreak
        'smarty',  # emdash, endash, pretty quotes
        SubscriptExtension(),
        SuperscriptExtension(),
    ]

    return mark_safe(markdown.markdown(force_unicode(value),
                                       extensions,
                                       enable_attributes=False))
