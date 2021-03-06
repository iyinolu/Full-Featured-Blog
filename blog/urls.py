from django.urls import path
from . import views
from .views import (PostListView, 
                    PostDetailView, 
                    PostCreateView, 
                    PostUpdateView,  
                    PostDeleteView
)

urlpatterns = [
    # maps to home view
    path('', views.about, name='blog-about'),   
    # maps to post detail view
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),  
    path('posts/new/', PostCreateView.as_view(), name='post-create'), 
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), 
    #maps to about view
    path('home/',PostListView.as_view(), name='blog-home')
]
  
# <app>/<model>_<view_type>.html