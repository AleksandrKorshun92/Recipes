from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import logging
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, LoginUserForm, RecipesForm, UpdateForm, SearchForm
from .models import Author, Recipes, RecipeCategoryLink, RecipeCategories


logger = logging.getLogger(__name__)

# def index(request):
#     logging.info('Заход на главную страницу')
#     username = request.user
#     context = {"title": "Главная страница", "us":username}
#     return render(request, "base.html", context)

#Функция добавления рецепта
def add_product(request):
    if request.method == 'POST':
        form = RecipesForm(request.POST, request.FILES)
        message = 'Ошибка в заполнении'
        if form.is_valid():
            if request.user.is_authenticated:
                username = request.user
                name = form.cleaned_data['Название_рецепта']
                description = form.cleaned_data['Описание_рецепта']
                cooking_instructions = form.cleaned_data['Инструкция_приготовления']
                cooking_time = form.cleaned_data['Время_приготовления']
                category = form.cleaned_data['Категория_рецепта']
                logger.info(f'Получили {name=}, {description=}, {cooking_instructions=}, {cooking_time= }')
                image = form.cleaned_data['Картинка_рецепта']
                recipes = Recipes(name=name, description=description, cooking_instructions=cooking_instructions, cooking_time=cooking_time,
                                   image=image, author=username)
                recipes.save()
                categorys = RecipeCategories.objects.get(name=category)
                product = Recipes.objects.get(pk=recipes.pk)
                category_link = RecipeCategoryLink(category=categorys)
                category_link.save()
                category_link.recipe.add(product)
                fs = FileSystemStorage()
                fs.save(image.name, image)
                message = 'РЕЦЕПТ СОХРАНЕН'

    else:
        form = RecipesForm()
        message = 'Заполните форму'
    return render(request, 'start1_app/add_recipes.html', {'form':
                                                     form, 'message': message})

# вывод рецептов авторизованного пользователя
@login_required
def display_user_recipes(request):
    current_user = request.user
    user_recipes = Recipes.objects.filter(author=current_user)
    dict_user_recipes = {}
    dict_image={}
    for recipes in user_recipes:
        recipes_dict = {"Название рецепта": recipes.name,
                     "Описание": recipes.description,
                     "Шаги приготовления":recipes.cooking_instructions,
                     "Время приготовления (в минутах)":recipes.cooking_time}
        recipes_temp=Recipes.objects.get(id=recipes.pk)
        catigories_temp = recipes_temp.in_order.all()
        for category in catigories_temp:
            recipes_dict['Категория рецепта'] = category.category.name
        dict_user_recipes[recipes.pk] = recipes_dict
        dict_image[recipes.pk] = recipes.image.url
    context = {
        'user_recipes': user_recipes,
        "current_user": current_user,
        "recipes": dict_user_recipes,
        'img': dict_image,
    }
    return render(request, "start1_app/recipes.html", context)


# поиск рецепта по номеру
@login_required
def update_user_recipes(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        message = 'Ошибка в заполненных данных (такого рецепта нет)'
        if form.is_valid():
            if request.user.is_authenticated:
                number = form.cleaned_data['Номер_рецепта']
                try:
                    product = Recipes.objects.get(pk=number)
                    message = f'Найден рецепт № {product.pk} {product.name}'
                    return render(request, 'start1_app/update2.html', {'form':
                                                                       form, 'message': message, "name": number, "prod":product})
                except:
                    print("Все таки тут")
                    logger.warning(f'Получили ошибку при обработки запроса (отсутствует номер рецепта или ввод не кооректный')
    else:
        form = SearchForm()
        message = 'Заполните форму'
    return render(request, 'start1_app/update.html', {'form':
                                                     form, 'message': message})

# Обновления рецепта (изменение)
def up(request, pk_recipet):
    product = Recipes.objects.get(pk=pk_recipet)
    if request.method == 'POST':
        form = UpdateForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            if request.user.is_authenticated:
                username = request.user
                name = form.cleaned_data['Название_рецепта']
                description = form.cleaned_data['Описание_рецепта']
                cooking_instructions = form.cleaned_data['Инструкция_приготовления']
                cooking_time = form.cleaned_data['Время_приготовления']
                category = form.cleaned_data['Категория_рецепта']
                logger.info(f'Получили {name=}, {description=}, {cooking_instructions=}, {cooking_time= }')
                image = form.cleaned_data['Картинка_рецепта']
                product.name = name
                product.description = description
                product.cooking_instructions = cooking_instructions
                product.cooking_time = cooking_time
                product.image = image
                product.save()
                categorys = RecipeCategories.objects.get(name=category)
                recipes = Recipes.objects.get(pk=product.pk)
                category_link = RecipeCategoryLink(category=categorys)
                category_link.save()
                category_link.recipe.add(recipes)
                fs = FileSystemStorage()
                fs.save(image.name, image)
                message = 'Продукт сохранён'
    else:
        form = UpdateForm()
        message = 'Заполните форму'
    return render(request, 'start1_app/update3.html', {'form':
                                                     form, 'message': message, "p":product})

# вывод подробно содержание рецепта (на вход принимает ключ рецепта)
def one_recipes(request, pk_recipet):
    product = Recipes.objects.get(pk=pk_recipet)
    img = product.image.url
    message = f'Рецепт № {product.pk} {product.name}'

    catigories_temp = product.in_order.all()
    for category in catigories_temp:
        c = category.category.name
    return render(request, 'start1_app/one_recipes.html',
                  {'message': message, "prod": product, 'img':img, 'c':c})


# вывод всех рецептов
def all_recipes(request):
    all_recipes = Recipes.objects.all()
    print(all_recipes)
    dict_user_recipes = {}
    dict_image={}
    for recipes in all_recipes:
        des = recipes.description
        des2 = f"{des[:150]}..." # ограничел описание рецепта
        recipes_dict = {"Название рецепта": recipes.name,
                     "Описание": des2,
                     "Время приготовления (в минутах)":recipes.cooking_time}

        dict_user_recipes[recipes.pk] = recipes_dict
        dict_image[recipes.pk] = recipes.image.url
    context = {
        "all_recipes":all_recipes,
        "recipes": dict_user_recipes,
        'img': dict_image,
    }
    return render(request, "start1_app/all_recipes.html", context)

# вывод 5 рецептов на главной странице
def index_recipes(request):
    all_recipes = Recipes.objects.all().order_by('id')[:14:3]
    dict_user_recipes = {}
    dict_image={}
    for recipes in all_recipes:
        des = recipes.description
        des2=f"{des[:150]}..." # ограничел описание рецепта
        recipes_dict = {"Название рецепта": recipes.name,
                     "Описание": des2,
                     "Время приготовления (в минутах)":recipes.cooking_time}

        dict_user_recipes[recipes.pk] = recipes_dict
        dict_image[recipes.pk] = recipes.image.url
    context = {
        "all_recipes":all_recipes,
        "recipes": dict_user_recipes,
        'img': dict_image,
    }
    return render(request, "base.html", context)

# Регистрация пользователя
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            user = form.save(commit=False)
            name = form.cleaned_data['username']
            user.save()
            birth_date = form.cleaned_data['birth_date']
            logger.info(f'Получили {name=}, {birth_date=}')
            author = Author.objects.create(user=user, birth_date=birth_date)
            author.save()
            return render(request,'start1_app/registracion_true.html', {"user_name": name}) # Перенаправление на страницу входа

    else:
        form = UserRegistrationForm()
        message = 'Заполните форму'
    return render(request, 'start1_app/registracion.html', {'form': form, 'message': message})

# Вход пользователя
def login_user(request):
    if request.method =='POST':
        form = LoginUserForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd["username"], password=cd['password'])
            if user and user.is_active:
                login(request,user)
                return render(request,'start1_app/login_true.html', {"user_name": cd["username"]})

    else:
        form = LoginUserForm()
        message = 'Заполните форму'
    return render(request, 'start1_app/login.html', {'form': form, 'message': message})

# Выход пользователя
def logout_user(request):
    logout(request)
    logger.info(f"произведен выход")
    return redirect('/')

