from django.contrib import admin
from .models import Recipes,Author,RecipeCategories,RecipeCategoryLink

class RecipesAdmin(admin.ModelAdmin):
    list_display = ["author", "name", "cooking_time", "register_date"]
    ordering = ["author", "name"]
    list_filter = ["author", "name"]
    search_fields = ['author', "name"]
    search_help_text = 'Поиск по полю автоп, название рецепта'

admin.site.register(Recipes, RecipesAdmin)
