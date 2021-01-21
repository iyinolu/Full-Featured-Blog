from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from users.models import Profile
from blog.models import Posts



def register(request):    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created, {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form":form})


@login_required
def profile(request):
    return render(request, "users/profile.html")


def user_profile(request, pk):
    user_details = Profile.objects.filter(id=pk).first()
    user = Profile.objects.filter(id=pk).first().user.id

    user_posts = Posts.objects.filter(author=user).order_by('-date_posted')
    paginator = Paginator(user_posts, 3)
    template = 'users/profile_detail.html'
    logged_user = str(request.user)
    return render(request, template, {'posts':user_posts, 'user_details': user_details, 'logged_user':logged_user})
        


def ProfileUpdate(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, "users/editProfile.html", context)


def my_logout(request):
    return logout_then_login(request)

