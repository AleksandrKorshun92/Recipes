import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Author

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(initial=datetime.date.today, widget=forms.DateInput(
        attrs={'class': 'form-control', 'type':'date'}))

    class Meta:
        model = get_user_model()
        fields = ['username', "last_name", 'email', "birth_date"]
        labels = {"username": "Логин", "last_name": "Фамилия", 'email':'Почта', "birth_date":"Дата рождения"}
        widgets = {"username": forms.TextInput(attrs={"class": "form-input"}),
                   "last_name": forms.TextInput(attrs={"class": "form-input"}),
                   'email': forms.EmailInput(attrs={"class": "form-input"})
        }


class LoginUserForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={"class": "form-input"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={"class": "form-input"}))

# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form_control",
#                                                                          "placeholder": "напишите название продукта"}))
#     describe = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
#     price = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     quantity = forms.IntegerField(min_value=18, widget=forms.NumberInput(attrs={'class': 'form-control'}))
#     image = forms.ImageField()

# class ImageForm(forms.Form):
#     image = forms.ImageField()

class RecipesForm(forms.Form):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Автор. Только зарегестрированные пользователи?!
    Название_рецепта = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form_control",
                                                                         "placeholder": "Напишите название "}))
    Описание_рецепта = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "placeholder": "Напишите описание блюда"}))
    Инструкция_приготовления = forms.CharField(widget=forms.Textarea(attrs={"class": "form_control",
                                                                         "placeholder": "Подробно напишите ингредиенты и шаги приготовления блюда"}))
    Время_приготовления = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control',  "placeholder": "Напишите время приготовления (в минутах)"}))
    Картинка_рецепта = forms.ImageField()
    Категория_рецепта = forms.ChoiceField(choices=[('Супы', 'Супы'),('Каши','Каши'), ('Гарниры','Гарниры'),('Напитки','Напитки'),('Десерты','Десерты')])

class SearchForm(forms.Form):
    # Название_рецепта = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form_control",
    #                                                                      "placeholder": "Напишите название рецепта, который надо изменить "}))
    Номер_рецепта = forms.IntegerField(min_value=1, widget=forms.NumberInput(
        attrs={'class': 'form-control', "placeholder": "Напишите номер рецепта, который надо изменить "}))

class UpdateForm(forms.Form):
    # author = models.ForeignKey(Author, on_delete=models.CASCADE)  # Автор. Только зарегестрированные пользователи?!
    Название_рецепта = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class":"form_control",
                                                                         "placeholder": "Напишите название "}))
    Описание_рецепта = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', "placeholder": "Напишите описание блюда"}))
    Инструкция_приготовления = forms.CharField(widget=forms.Textarea(attrs={"class": "form_control",
                                                                         "placeholder": "Подробно напишите ингредиенты и шаги приготовления блюда"}))
    Время_приготовления = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control',  "placeholder": "Напишите время приготовления (в минутах)"}))
    Картинка_рецепта = forms.ImageField()
    Категория_рецепта = forms.ChoiceField(choices=[('Супы', 'Супы'),('Каши','Каши'), ('Гарниры','Гарниры'),('Напитки','Напитки'),('Десерты','Десерты')])