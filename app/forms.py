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

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'

  def clean_username(self):
      username = self.cleaned_data['username']
      get_user_model().objects.filter(username=username, is_active=False).delete()
      return username

  def clean_email(self):
      email = self.cleaned_data['email']
      get_user_model().objects.filter(email=email, is_active=False).delete()
      return email


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
