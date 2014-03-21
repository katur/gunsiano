from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from protocols.models import Protocol


@login_required
def protocols(request):
    """
    Page listing protocols
    """
    protocols = Protocol.objects.all().order_by('title_markdown')

    dictionary = {
        'protocols': protocols,
    }
    return render_to_response('protocols.html', dictionary,
                              context_instance=RequestContext(request))


@login_required
def protocol(request, title_url):
    """
    Page listing protocol
    """
    protocol = get_object_or_404(Protocol, title_url=title_url)

    dictionary = {
        'protocol': protocol,
    }
    return render_to_response('protocol.html', dictionary,
                              context_instance=RequestContext(request))
