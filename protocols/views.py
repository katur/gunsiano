from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from protocols.models import Protocol


@login_required
def protocols(request):
    """
    Page listing protocols
    """
    protocols = Protocol.objects.all().order_by('title')
    return render(request, 'protocols.html', {'protocols': protocols})


@login_required
def protocol(request, slug):
    """
    Page listing protocol
    """
    protocol = get_object_or_404(Protocol, slug=slug)
    return render(request, 'protocol.html', {'protocol': protocol})
