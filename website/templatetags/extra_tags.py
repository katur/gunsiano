import markdown
from markdown.inlinepatterns import SimpleTagPattern

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils import formats
from django.utils.safestring import mark_safe


SUBSCRIPT_RE = r'(\~)([^\~]*)\2'  # e.g. ~2~
SUPERSCRIPT_RE = r'(\^)([^\^]*)\2'  # e.g. ^2^


register = template.Library()


class SubscriptExtension(markdown.Extension):
    """ Subscript Extension for Python-Markdown. """

    def extendMarkdown(container, md, md_globals):
        """ Replace subscript with SubscriptPattern """
        md.inlinePatterns.add('subscript',
                              SimpleTagPattern(SUBSCRIPT_RE, 'sub'),
                              '<not_strong')


class SuperscriptExtension(markdown.Extension):
    """ Superscript Extension for Python-Markdown. """

    def extendMarkdown(container, md, md_globals):
        """ Replace superscript with SuperscriptPattern """
        md.inlinePatterns.add('superscript',
                              SimpleTagPattern(SUPERSCRIPT_RE, 'sup'),
                              '<not_strong')


@register.filter(is_safe=True)
@stringfilter
def enhanced_markdown(text):
    """
    Render markdown with various extensions.
    """
    extensions = [
        'nl2br',  # more intuitive linebreak
        'smarty',  # emdash, endash, pretty quotes
        SubscriptExtension(),
        SuperscriptExtension(),
    ]

    return mark_safe(markdown.markdown(force_unicode(text),
                                       extensions,
                                       enable_attributes=False))


@register.filter(is_safe=True)
def get_hover_string(container):
    """
    Get information to display when hovering over a storage container.
    """
    if container.stock and get_prep_string(container.stock):
        return get_prep_string(container.stock)

    result = ''
    if container.owner:
        result += container.owner.get_full_name()
    if container.owner and container.notes:
        result += ' ('
    if container.notes:
        result += container.notes
    if container.owner and container.notes:
        result += ')'

    return result


@register.filter(is_safe=True)
def get_thaw_string(container):
    """
    Get a storage container's thaw details.
    """
    if not (container.is_thawed):
        return ''

    result = 'Thawed'
    if container.thawed_by:
        result += ' by {}'.format(container.thawed_by.get_full_name())
    if container.date_thawed:
        result += ' on {}'.format(formats.date_format(container.date_thawed))
    if container.thaw_results:
        result += ' ({})'.format(container.thaw_results)
    return result


@register.filter(is_safe=True)
def get_prep_string(stock):
    """
    Get a stock's preparation details.
    """
    result = 'Stock'
    if not (stock.prepared_by or stock.date_prepared):
        return result

    result += ' frozen'
    if stock.prepared_by:
        result += ' by {}'.format(stock.prepared_by.get_full_name())
    if stock.date_prepared:
        result += ' on {}'.format(formats.date_format(stock.date_prepared))
    return result


@register.filter(is_safe=True)
def get_receipt_string(worm):
    """
    Get a worm's receipt details.
    """
    if not (worm.received_by or worm.received_from or
            worm.date_received):
        return ''

    result = 'Line received'
    if worm.received_by:
        result += ' by {}'.format(worm.received_by.get_full_name())
    if worm.received_from:
        result += ' from {}'.format(worm.received_from)
    if worm.date_received:
        result += ' on {}'.format(formats.date_format(worm.date_received))
    return result
