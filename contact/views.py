from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def index(request):

    context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        }
    return render(request, 'contact/index.html', context)