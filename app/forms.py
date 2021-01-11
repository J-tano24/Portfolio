# カスタムユーザーモデルを参照するには、get_user_model関数をインポート
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
      model = get_user_model() 
      fields = ('username', 'email',)