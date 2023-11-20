
from django.shortcuts import render, get_list_or_404, get_object_or_404
# from utils.recipes.factory import make_recipe
from recipes.models import Recipe
from django.http import Http404

# from django.http import HttpResponse
# Create your views here.

# def sobre(request):
#     return HttpResponse("SOBRE")


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, is_published=True).order_by('-id')

    # if not recipes:
    #     raise Http404('Not found :(')

    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True).order_by('-id'))

    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'category': recipes[0].category
    })


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     pk=id, is_published=True).order_by('-id').first()
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        "is_detail_page": True,
    })


def search(request):
    search_term = request.GET.get('q', '').strip()

    if not search_term:
        raise Http404()

    return render(request, 'recipes/pages/search.html', context={
        'page_title': f'Search for "{search_term}"',
        'search_term': search_term},)
