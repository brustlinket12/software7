from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Blog
from django.http import HttpResponseForbidden


class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'tag', 'cover_image']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})

# clase pa borrar un blog, DeleteView hace eso
# en realidad no los "borra", si no que los "oculta"
# así no se borra nada en la base
class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogapp:blog_list')

    def get_queryset(self):
        return Blog.all_objects.filter(is_deleted=False)

    def test_func(self):
        return self.request.user == self.get_object().author
    
# clase que edita los blogs, UpdateView hace todo
# donde pone 'pk' es la primary key del blog q se va a editar, asiq no se pierde nada
class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView ):
    model = Blog
    fields = ['title', 'content', 'tag']
    template_name = 'blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user == self.get_object().author

class ReviewCreateView(LoginRequiredMixin, CreateView): #Pide usuario logeado para crear review
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'
    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Verificar si el usuario ya ha dejado una reseña para este blog
        if self.request.user.is_authenticated and Review.objects.filter(blog=self.blog, reviewer=self.request.user).exists():
            return self.handle_no_permission()  # Redirige directamente si ya existe
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.error(self.request, 'Ya has dejado una reseña para esta publicación.')
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})

    def handle_no_permission(self):
        messages.error(self.request, 'Ya has dejado una reseña para esta publicación.')
        return redirect(self.get_success_url())

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs['review_pk'])


    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.blog.pk})

    def test_func(self):
        return self.request.user == self.get_object().reviewer
    
def delete_review(request, blog_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, blog_id=blog_pk)

    if request.user == review.reviewer:
        review.is_deleted = True  # Cambia el estado a eliminado
        review.save()
        return redirect('blogapp:blog_detail', pk=blog_pk)
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar esta reseña.")

class CommentCreateView(LoginRequiredMixin, CreateView): #Pide usuario logeado para crear review
    model = Comment
    fields = ['content']
    template_name = 'blogapp/comment_form.html'

    def form_valid(self, form):
        form.instance.commenter = self.request.user
        form.instance.review_id = self.kwargs['review_pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['blog_pk']})

# clase del perfil de usuario, casi igual q Bloglistview
class ProfileView(ListView):
    model = Blog
    template_name = 'blogapp/profile.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return Blog.objects.filter(author=self.request.user)

class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1','password2']
def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password) 
            if user is not None:
                login(request, user)
                return redirect('blogapp:blog_list')
    else:
        form = RegisterUser()
    return render(request, 'blogapp/create_user.html', {'form': form})

class LoginUser(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

def signin(request):
        if request.method == 'POST':
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'login.html',{
                'form': LoginUser(request.POST),
                'error': 'El usuario o la contraseña son incorrectos'
            })
            else:
                login(request, user)
                return redirect('blogapp:blog_list')
            return render(request, 'login.html',{
            'form': LoginUser(request.POST)
            })
        else:
            return render(request, 'login.html',{
            'form': LoginUser(request.POST),
            'error': 'El usuario o la contraseña son incorrectos'
            })

def signout(request):
    logout(request)
    return redirect('blogapp:blog_list')


# Cambio de Contraseña
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("La nueva contraseña y la confirmación no coinciden.")

        return cleaned_data

class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('blogapp:password_change_done')
    template_name = ('blogapp/password_change_form.html')

    def form_invalid(self, form):
        # Si el formulario es válido, la contraseña se cambia
        return self.render_to_response(self.get_context_data(form=form))


    def form_invalid(self, form):
        # Si el formulario no es válido, la página se reinicia
        return self.render_to_response(self.get_context_data(form=form))

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = ('blogapp/password_change_done.html')

    
def blog_list_view(request):
    query = request.GET.get('busqueda')
    if query:
        if query.startswith('#'):
            tag = query[1:]
            if tag:
                blog_list = Blog.objects.filter(tag__title__icontains=tag).distinct()
            else:
                blog_list = Blog.objects.all()
        else:
            blog_list = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).distinct()
    else:
        blog_list = Blog.objects.all()

    paginator = Paginator(blog_list, 5)  # 5 blogs por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'page_obj': page_obj, 'object_list': page_obj})

def my_view(request):
    # Generamos una lista de números del 0 al 59
    range_numbers = list(range(60))
    return render(request, 'tu_template.html', {'range_numbers': range_numbers})