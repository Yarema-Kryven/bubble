from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def logout_view(request):
    #Логаут юзера
    logout(request)
    return HttpResponseRedirect(reverse('bubbleapp:index'))


def register(request):
    """Реєстрація нового користувача"""
    if request.method != 'POST':
        #Display blank registration form
        form=UserCreationForm()
    else:
        #Обробка заповненої форми
        form=UserCreationForm(data=request.POST)
    if form.is_valid():
        new_user=form.save()
        #Виконання входу та перенаправлення на домашню сторінку
        authenticated_user=authenticate(username=new_user.username,password=request.POST['password1'])
        login(request,authenticated_user)
        return HttpResponseRedirect(reverse('home'))
    context={'form':form}
    return render(request,'users/register.html',context)
