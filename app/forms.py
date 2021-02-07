# カスタムユーザーモデルを参照するには、get_user_model関数をインポート
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from .models import Photo
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = get_user_model() 
    fields = ('username', 'email',)

  def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for field in self.fields.values():
          field.widget.attrs['class'] = 'form-control'
          field.widget.attrs['placeholder'] = field.label

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
      # placeholderにフィールドのラベルを入れる
      field.widget.attrs['placeholder'] = field.label

class MyPasswordChangeForm(PasswordChangeForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
      field.widget.attrs['placeholder'] = field.label

class MyPasswordResetForm(PasswordResetForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
      field.widget.attrs['placeholder'] = field.label

class MySetPasswordForm(SetPasswordForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields.values():
      field.widget.attrs['class'] = 'form-control'
      field.widget.attrs['placeholder'] = field.label

class PhotoForm(ModelForm):
  class Meta:
    model = Photo
    fields = ['image', 'category', 'place_name', 'lat', 'lng']
