from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
  path('', views.index, name='index'),
  path('users/<int:pk>/', views.users_detail, name='users_detail'),
  path('photos/new/', views.photos_new, name='photos_new'),
  path('photos/<int:pk>/', views.photos_detail, name='photos_detail'),
  path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'),
  path('photos/<str:category>/', views.photos_category, name='photos_category'),
  path('fav_photos/', views.fav_photos, name='fav_photos'),
  path('fav_photos_status/', views.fav_photos_status, name='fav_photos_status'),

  path('login/', views.Login.as_view(), name='login'),
  path('logout/', views.Logout.as_view(), name='logout'),
  
 
]