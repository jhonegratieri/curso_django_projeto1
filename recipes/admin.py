from django.contrib import admin
from .models import Category, Recipe
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


# O comando abaixo é equivalente ao decorador @ @admin.register(Category)
# admin.site.register(Category, CategoryAdmin)
