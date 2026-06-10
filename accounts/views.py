
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login

# Create your views here.
def register( request):
    """注册新用户"""
    if request.method != 'POST':
        """显示空的注册表单"""
        form = UserCreationForm()
    else:
        """处理填写的表单"""
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form': form}
    return render(request, 'registration/register.html', context)