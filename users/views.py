from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.views.generic import DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from ..users.models import Profile
from ..blog.models import Posts


def Register(request):    
    """View to display register page required for creating a
    user account
    """
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
def ProfileView(request):
    """Display user profile information.
    """
    return render(request, "users/profile.html")


def UserProfile(request, pk):
    """ Display user profile information and posts on the same 
        view.
    """
    pk = int(pk)
    # get profile of the parsed primary key
    user_details = Profile.objects.filter(id=pk).first()
    # get user id from profile object
    user = Profile.objects.filter(id=pk).first().user.id

    user_posts = Posts.objects.filter(author=user).all().order_by('-date_posted')
    paginator = Paginator(user_posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    template = 'users/profile_detail.html'
    logged_user = str(request.user)
    return render(request, template, {'posts':user_posts, 
                                    'user_details': user_details, 
                                    'logged_user':logged_user,
                                    'page_obj': page_obj
                                    
    })
        


def ProfileUpdate(request, *args):
    """ Display profile update form that can only be accessed
    by the current logged in user.
    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('user-posts', request.user.profile.id)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, "users/editProfile.html", context)


def MyLogout(request):
    return logout_then_login(request)

