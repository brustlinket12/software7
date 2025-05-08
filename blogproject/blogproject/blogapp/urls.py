from django.urls import path, include
from .views import BlogListView, BlogDetailView, ReviewCreateView, CommentCreateView, BlogCreateView, BlogDeleteView, BlogUpdateView, ProfileView, ChangePasswordView, PasswordChangeDone
from .views import register, signin, signout
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views
from .views import blog_list_view, delete_review
from blogapp.views import ReviewUpdateView




from django.contrib import admin

app_name = 'blogapp'


urlpatterns = [
    path('', blog_list_view, name='blog_list'),
    path('blog/add/', BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/review/', ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('blog/<int:pk>/delete/', BlogDeleteView.as_view(), name='delete_blog'),
    path('blog/<int:pk>/edit/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/edit/', ReviewUpdateView.as_view(), name='edit_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/delete/', delete_review, name='delete_review'),

    path('register/', register, name='create_user'),
    path('login/', signin, name='login'),
    path('logout/', signout, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDone.as_view(), name='password_change_done'),

    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
