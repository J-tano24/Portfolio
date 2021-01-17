# カスタムユーザーモデルを参照するには、get_user_model関数をインポート
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Photo

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = get_user_model() 
    fields = ('username', 'email',)

class PhotoForm(ModelForm):
  class Meta:
    model = Photo
    fields = ['title', 'place_name', 'lat', 'lng', 'image', 'category']