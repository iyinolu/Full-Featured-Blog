"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as users_views
from django.conf import settings
from django.conf.urls.static import static 
# from users.views import ProfileDetailView


urlpatterns = [
    path('admin/', admin.site.urls, name='app-admin'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'), # Login view route
    path('logout/', users_views.MyLogout, name='logout'), # Logout view route
    path('', include('blog.urls')),  # Blog url route
    path('register/', users_views.Register, name='register'), # Register view route
    path('editprofile/', users_views.ProfileUpdate, name='profile-update'), # EditProfile view route
    path('profile/', users_views.ProfileView, name='profile'), # User profile view route
    path('user/<int:pk>', users_views.UserProfile, name='user-posts') # User profile and posts route
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    
