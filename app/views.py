from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
def index(request):
  return render(request, 'app/index.html')

# def users_detail(request, pk):
#   user = get_object_or_404(User, pk=pk)
#   return render(request, 'app/users_detail.html', {'user':user})