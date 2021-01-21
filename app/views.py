from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login 
from .forms import CustomUserCreationForm
from .models import Photo, Category
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
  
def index(request):
  photos = Photo.objects.all().order_by('-created_at')
  return render(request, 'app/index.html', {'photos': photos})

def users_detail(request, pk):
  user = get_object_or_404(get_user_model(), pk=pk)
  photos = user.photo_set.all().order_by('-created_at')
  return render(request, 'app/users_detail.html', {'user':user, 'photos':photos})

def signup(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
      new_user = form.save()
      input_username = form.cleaned_data['username']
      input_email = form.cleaned_data['email'] 
      input_password = form.cleaned_data['password1'] 
      new_user = authenticate(username=input_username, email=input_email, password=input_password)
      if new_user is not None:
        login(request, new_user) 
        return redirect('app:index')
  else:
    form = CustomUserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def photos_new(request):
  if request.method == "POST":
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():
      # commit=Falseにすることで、DBには一旦保存しない。この段階でphotoインスタンスのuserフィールドに入れる値が決まっていないから。
      photo = form.save(commit=False)
      photo.post_user = request.user
      photo.save()
      messages.success(request, "投稿が完了しました！")
      return redirect('app:users_detail', pk=request.user.pk)
  else:
    form = PhotoForm()
  return render(request, 'app/photos_new.html', {'form': form})

def photos_detail(request, pk):
  photo = get_object_or_404(Photo, pk=pk)
  return render(request, 'app/photos_detail.html', {'photo': photo})

@require_POST
def photos_delete(request, pk):
  photo = get_object_or_404(Photo, pk=pk)
  photo.delete()
  return redirect('app:users_detail', request.user.id)

def photos_category(request, category):
  # title(Categoryのtitle、つまりcategory)がURLの文字列と一致するCategoryインスタンスを取得。
  category = Category.objects.get(title=category)
  # 取得したCategoryに属するPhoto一覧を取得。逆参照？
  photos = Photo.objects.filter(category=category).order_by('-created_at')
  return render(request, 'app/index.html', {'photos':photos, 'category': category})
  
@login_required
@require_POST
def fav_photos_status(request):
  photo = get_object_or_404(Photo, pk=request.POST["photo_id"])
  user = request.user
  if photo in user.fav_photos.all():
    user.fav_photos.remove(photo)
  else:
    user.fav_photos.add(photo)
  return redirect('app:photos_detail', pk=photo.id)

@login_required
def fav_photos(request):
  user = request.user
  photos = user.fav_photos.all()
  return render(request, 'app/index.html', {'photos': photos})