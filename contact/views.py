from django.shortcuts import render


# view for relatively static contact page
def index(request):

    # build context object
    context = {
            'breadcrumbs': request.get_full_path()[1:-1].split('/'),
        }
    return render(request, 'contact/index.html', context)