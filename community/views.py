from django.shortcuts import render
from .models import CommunitySection

# Create your views here.


def community_view(request):
    sections = CommunitySection.objects.all()
    context = {'sections': sections}
    return render(request, 'community.html', context)
