from django.shortcuts import render


def home_view(request):
    context = {
        'title': 'Mashaudit'
    }
    return render(request, 'base.html', context)
