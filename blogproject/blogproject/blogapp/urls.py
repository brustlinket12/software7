from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

# Gracias a 'views/__init__.py', podemos importar todo de forma limpia desde el paquete 'views'.
# Ya no necesitamos una larga lista de importaciones.
from . import views

app_name = 'blogapp'

urlpatterns = [
    # URLs de Blogs
    # Usamos BlogListView directamente. Ya integra la lógica de búsqueda y paginación.
    path('', views.BlogListView.as_view(), name='blog_list'), 
    path('blog/add/', views.BlogCreateView.as_view(), name='add_blog'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blog/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='edit_blog'),
    path('blog/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='delete_blog'),

    # URLs de Reviews
    path('blog/<int:pk>/review/', views.ReviewCreateView.as_view(), name='add_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/edit/', views.ReviewUpdateView.as_view(), name='edit_review'),
    path('blog/<int:blog_pk>/review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    
    # URLs de Comments
    path('blog/<int:blog_pk>/review/<int:review_pk>/comment/', views.CommentCreateView.as_view(), name='add_comment'),

    # URLs de Autenticación y Perfil
    # Mantenemos tus nombres de URL para consistencia ('create_user' en lugar de 'register')
    path('register/', views.register, name='create_user'), 
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('password-change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),

    # URLs de paquetes de terceros y admin (se mantienen igual)
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
]

# Configuración para archivos media en modo DEBUG (se mantiene igual)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)