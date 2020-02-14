from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import views as auth_views

def login(request):
  print(request.user.is_authenticated)
  if request.user.is_authenticated:
    return redirect('/profile')
  return auth_views.LoginView.as_view(template_name = 'users/login.htm')(request)


def register(request):
  if request.method == 'POST':
    form = UserRegisterForm(request.POST)
    if form.is_valid():
      form.save()
      # username = form.cleaned_data.get('username')
      messages.success(request, f'Your account has been created! You are now able to log in')
      return redirect('login')
  else:
    form = UserRegisterForm()
  return render(request, 'users/register.htm', {'form': form})

@login_required
def profile(request):
  if request.method == 'POST':
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request, f'Your account has been updated!')
      return redirect('profile')
  else:
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)

  context = {
    'u_form': u_form,
    'p_form': p_form,
  }
  return render(request, 'users/profile.htm', context=context)

