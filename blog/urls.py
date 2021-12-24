from django.urls import path
from .views import (
    PostListView,
   
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    AddCommentView
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('contact/', views.contactview, name='blog-contact'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add_comment'),
]