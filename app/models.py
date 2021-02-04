from django.db import models
# CustomUserモデルをimportする時のget_user_model
# 参照：https://djangobrothers.com/blogs/referencing_the_user_model/
from django.contrib.auth import get_user_model

class Category(models.Model):
  title = models.CharField(max_length=20)
  def __str__(self):
    return self.title

class Photo(models.Model):
  post_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
  # photoservice_p/media/photosに自動で保存される。
  image = models.ImageField(upload_to='photos') 
  category = models.ForeignKey(Category, on_delete=models.PROTECT) 
  place_name = models.CharField(max_length=100)
  # 緯度経度フィールド（https://stackoverflow.com/questions/57131896/how-do-i-save-google-places-location-to-django-models）
  lat = models.DecimalField(max_digits=30, decimal_places=7)
  lng = models.DecimalField(max_digits=30, decimal_places=7)
  created_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.place_name
