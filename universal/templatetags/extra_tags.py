import markdown
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def enhanced_markdown(value):
    extensions = [
        # for newline to create line break / more intuitive
        # "nl2br",

        # for emdash, endash, pretty quotes
        "smartypants",

        "subscript",
        "superscript",
    ]

    return mark_safe(markdown.markdown(
        force_unicode(value), extensions, safe_mode=True,
        enable_attributes=False))
