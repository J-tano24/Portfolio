from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
# 下のライブラリは？
from django.utils.translation import ugettext_lazy as _
from .models import User

"""User 情報を変更するフォーム"""
class MyUserChangeForm(UserChangeForm):
  class Meta:
    model = User
    fields = '__all__'# 全ての情報を変更可能

"""User を作成するフォーム"""
class MyUserCreationForm(UserCreationForm): 
  class Meta:
    model = User
    fields = ('username', 'email',) # email とパスワードが必要

"""カスタムユーザーモデルの Admin""" 
class MyUserAdmin(UserAdmin):
  # ↓Userのリンクをクリックした時の詳細画面で確認できる。
  fieldsets = (
    (None, {'fields': ('username', 'email', 'password')}), 
    (_('Permissions'), {'fields': ('is_active', 'is_staff','is_superuser', 'groups', 'user_permissions')}),
    (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
  )
  add_fieldsets = (
    (None, {'classes': ('wide',),
    'fields': ('username', 'email', 'password1', 'password2'),}),
  )
  form = MyUserChangeForm
  add_form = MyUserCreationForm
  list_display = ('username', 'email', 'is_staff')
  list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
  search_fields = ('username', 'email',)
  ordering = ('username', 'email',)

admin.site.register(User, MyUserAdmin)