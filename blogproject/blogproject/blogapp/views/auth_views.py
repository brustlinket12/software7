from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..forms import RegisterUserForm, LoginForm, ChangePasswordForm
from ..models import Blog

# Vista para registro
def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blogapp:blog_list')
    else:
        form = RegisterUserForm()
    return render(request, 'blogapp/create_user.html', {'form': form})

# Vista para login 
def signin(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
           
            return redirect(request.GET.get('next', 'blogapp:blog_list'))
        else:
          
            return render(request, 'blogapp/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'blogapp/login.html', {'form': form})

# Vista para logout
def signout(request):
    logout(request)
    return redirect('blogapp:blog_list')

# Vistas para cambiar contraseña
class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('blogapp:password_change_done')
    template_name = 'blogapp/password_change_form.html'

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'blogapp/password_change_done.html'

# Vista de perfil de usuario
class ProfileView(LoginRequiredMixin, ListView):
    model = Blog
    template_name = 'blogapp/profile.html'
    context_object_name = 'user_blogs'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user, is_deleted=False)