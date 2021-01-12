from django.db import models
# CustomUserモデルをimportする時のget_user_model
# 参照：https://djangobrothers.com/blogs/referencing_the_user_model/
from django.contrib.auth import get_user_model

class Category(models.Model):
  title = models.CharField(max_length=20)
  def __str__(self):
    return self.title

class Photo(models.Model):
  title = models.CharField(max_length=20)
  place_name = models.CharField(max_length=100)
  # comment = models.TextField(blank=True)
  image = models.ImageField(upload_to='photos') 
  # photoservice_p/media/photosに自動で保存される。
  category = models.ForeignKey(Category, on_delete=models.PROTECT) 
  post_user = models.ForeignKey('users.User', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return self.title
