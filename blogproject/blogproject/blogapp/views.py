from django.views.generic import ListView, DetailView, CreateView, FormView
from django.urls import reverse_lazy
from .models import Blog, Review, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect

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

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


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

#TODO: redireccionar el usuario a la pagina de registro o la de inicio de sesión
#TODO: si este intenta crear un blog, review o comentario sin haber iniciado sesión (por eso el LoginRequiredMixin de arriba)


# crear usuarios
class RegisterUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

def register(request):
    if request.method == 'POST':
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogapp/base.html')
    else:
        form = RegisterUser()

    return render(request, 'blogapp/create_user.html', {'form': form})