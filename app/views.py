from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login 
from .forms import CustomUserCreationForm 

def index(request):
  return render(request, 'app/index.html')

def 

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

