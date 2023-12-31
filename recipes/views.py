import os

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views.generic import ListView

from recipes.models import Recipe
from utils.pagination import make_pagination

# from utils.recipes.factory import make_recipe
# from django.core.paginator import Paginator
# from django.http import HttpResponse


# def sobre(request):
#     return HttpResponse("SOBRE")


PER_PAGE = int(os.environ.get("PER_PAGE", 3))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = "recipes"
    ordering = ["-id"]
    template_name = "recipes/pages/home.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request, ctx.get("recipes"), PER_PAGE
        )
        ctx.update(
            {
                "recipes": page_obj,
                "pagination_range": pagination_range,
            },
        )
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__id=self.kwargs.get("category_id"))
        return qs


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get("q", "")
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) | Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get("q", "")

        ctx.update(
            {
                "page_title": f'Search for "{search_term}" |',
                "search_term": search_term,
                "additional_url_query": f"&q={search_term}",
            }
        )

        return ctx


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by("-id")

    page_obj, pagination_range = make_pagination(
        request, queryset=recipes, per_page=PER_PAGE, qty_pages=4
    )  # noqa: E501

    return render(
        request,
        "recipes/pages/home.html",
        context={"recipes": page_obj, "pagination_range": pagination_range},
    )


def category(request, category_id):
    # recipes = Recipe.objects.filter(
    #     category__id=category_id, is_published=True).order_by('-id')

    # if not recipes:
    #     raise Http404('Not found :(')

    recipes = get_list_or_404(
        Recipe.objects.filter(category__id=category_id, is_published=True).order_by(
            "-id"
        )
    )

    page_obj, pagination_range = make_pagination(
        request,
        queryset=recipes,
        per_page=PER_PAGE,
        qty_pages=4,
    )  # noqa: E501

    return render(
        request,
        "recipes/pages/category.html",
        context={
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "category": recipes[0].category,
        },
    )


def recipe(request, id):
    # recipe = Recipe.objects.filter(
    #     pk=id, is_published=True).order_by('-id').first()
    recipe = get_object_or_404(
        Recipe,
        pk=id,
        is_published=True,
    )
    return render(
        request,
        "recipes/pages/recipe-view.html",
        context={
            "recipe": recipe,
            "is_detail_page": True,
        },
    )


def search(request):
    search_term = request.GET.get("q", "").strip()

    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(Q(title__icontains=search_term) | Q(description__icontains=search_term)),
        is_published=True,
    ).order_by("-id")

    page_obj, pagination_range = make_pagination(
        request, queryset=recipes, per_page=PER_PAGE, qty_pages=4
    )  # noqa: E501

    return render(
        request,
        "recipes/pages/search.html",
        context={
            "page_title": f'Search for "{search_term}"',
            "search_term": search_term,
            "recipes": page_obj,
            "pagination_range": pagination_range,
            "additional_url_query": f"&q={search_term}",
        },
    )


# python -c
# "import string as s;from random import SystemRandom as
# sr;print(''.join(sr().choices(s.ascii_letters +
# s.punctuation, k=64)))"
