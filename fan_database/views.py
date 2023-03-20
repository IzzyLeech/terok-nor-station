from django.shortcuts import render
from .models import Season


def index_view(request):
    seasons = Season.objects.all()
    context = {'seasons': seasons}
    return render(request, 'index.html', context)



