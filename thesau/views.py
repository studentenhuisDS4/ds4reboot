from django.shortcuts import render


# view for thesau page
def index(request):

    context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        }
    return render(request, 'thesau/index.html', context)