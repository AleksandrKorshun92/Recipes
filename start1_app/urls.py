from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (register, login_user, logout_user,
                    add_product, display_user_recipes, all_recipes, index_recipes,
                    update_user_recipes, up, one_recipes)



urlpatterns = [
    path("add/", add_product, name="add_product"),
    path("my_recipes/", display_user_recipes, name="display_user_recipes"),
    path("register/", register, name="register"),
    path("login/", login_user, name='login'),
    path("logout/", logout_user, name='logout'),
    path("all_recipes/", all_recipes, name='all_recipes'),
    path("", index_recipes, name='index_recipes'),
    path("update_user_recipes/", update_user_recipes, name='update_user_recipes'),
    path("up/<int:pk_recipet>/", up, name="up"),
    path("one_recipes/<int:pk_recipet>/", one_recipes, name="one_recipes"),
]