from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegrityError

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content']
    template_name = 'blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})



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