
from django.shortcuts import render
# from django.http import HttpResponse
# Create your views here.

# def sobre(request):
#     return HttpResponse("SOBRE")


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Jhonatan',
        })


def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
                  'name': 'Jhonatan',
                  })

