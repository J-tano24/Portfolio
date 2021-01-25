from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model, authenticate, login 
from .forms import CustomUserCreationForm, LoginForm
from .models import Photo, Category
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView
)
from django.views import generic
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest
from django.template.loader import render_to_string
  
def index(request):
  photos = Photo.objects.all().order_by('-created_at')
  return render(request, 'app/index.html', {'photos': photos})

# 以下、クラスで定義しているViewは、Djangoのツールになる。
class Login(LoginView):
    form_class = LoginForm
    template_name = 'app/login.html'
    # 他関数でreturn render(request, 'app/index.html', {'photos': photos})としているのを上記２行で記載。

class Logout(LogoutView):
    template_name = 'app/top.html'

class UserCreate(generic.CreateView):
    template_name = 'app/user_create.html' 
    form_class = CustomUserCreationForm

    # form_valid関数は，POSTされたときに呼ばれる関数。if form.is_valid()
    def form_valid(self, form): 
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単、is_active=Falseで仮登録。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # アクティベーションURLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain 
        # URLを生成するのに必要な情報をcontextにまとめる。
        context = {
            'protocol': self.request.scheme, # http
            'domain': domain, # 127.0.0.1;8000
            'token': dumps(user.pk),
            'user': user,
        }

        # Djangoの設定で、render引数のURLパスを指定するときは、app/template/に続けてかく必要があるため、下記の場合、mail_templateは、app/template/appの中に入れる必要がある。 
        subject = render_to_string('app/mail_template/create/subject.txt', context)
        message = render_to_string('app/mail_template/create/message.txt', context)
        
        # email_userは、userオブジェクト（AbstractUser）のメソッド。条件の引数を指定すれば、メールを送付してくれる。
        user.email_user(subject, message)
        return redirect('app:user_create_done')

class UserCreateDone(generic.TemplateView):
    template_name = 'app/user_create_done.html'

class UserCreateComplete(generic.TemplateView):
    template_name = 'app/user_create_complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = get_user_model().objects.get(pk=user_pk)
            except get_user_model().DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

def users_detail(request, pk):
  user = get_object_or_404(get_user_model(), pk=pk)
  photos = user.photo_set.all().order_by('-created_at')
  return render(request, 'app/users_detail.html', {'user':user, 'photos':photos})

@login_required
def photos_new(request):
  # breakpoint() この関数が実行されているか検証
  if request.method == "POST":
    form = PhotoForm(request.POST, request.FILES)
    breakpoint() #POSTされているか検証
    if form.is_valid():
      breakpoint() #form.is_validになっているか検証
      photo = form.save(commit=False)
      photo.post_user = request.user
      photo.save()
      messages.success(request, "投稿が完了しました！")
    return redirect('app:users_detail', pk=request.user.pk)
    # ↑このreturnは、129行目が実行されれば、trueでもfalseでも実行される。
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