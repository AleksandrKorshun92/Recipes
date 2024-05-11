from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # bio = models.TextField(max_length=500, blank=True)
    # location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

class Recipes(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name="recipts",
                               null=True, default=None)  # Автор
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField()
    cooking_instructions = models.CharField(max_length=100) # Шаги приготовления
    cooking_time = models.IntegerField()  # Время приготовления (в минутах)
    image = models.ImageField(upload_to='recipe_images', default='default_image.jpg')  # Изображение
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Рецепт {self.name} описание {self.description}"
class RecipeCategories(models.Model):
    name = models.CharField(max_length=64, blank=False)
    description = models.TextField()


class RecipeCategoryLink(models.Model):
    category = models.ForeignKey(RecipeCategories, on_delete=models.CASCADE)
    recipe = models.ManyToManyField(Recipes, related_name="in_order")