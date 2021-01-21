# カスタムユーザーモデルを参照するには、get_user_model関数をインポート
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Photo
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = get_user_model() 
    fields = ('username', 'email',)

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label  # placeholderにフィールドのラベルを入れる

class PhotoForm(ModelForm):
  class Meta:
    model = Photo
    fields = ['place_name', 'lat', 'lng', 'image', 'category']
