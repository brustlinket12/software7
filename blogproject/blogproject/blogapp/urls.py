from django.urls import path
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, BlogDeleteView
from .views import register, signin, signout, profile

app_name = 'blogapp'


urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='delete_blog'),

    path('register/', register, name='create_user'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
    path('profile/', profile, name='profile'),
]