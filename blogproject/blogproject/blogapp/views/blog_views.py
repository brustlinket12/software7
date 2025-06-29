from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

from ..models import Blog # Usamos '..' para importar desde el directorio padre (blogapp)

class BlogListView(ListView):
    model = Blog
    template_name = 'blogapp/blog_list.html'
    context_object_name = 'object_list'
    paginate_by = 5 # Manera más limpia de paginar en ListView

    def get_queryset(self):
        query = self.request.GET.get('busqueda')
        if query:
            if query.startswith('#'):
                tag = query[1:]
                if tag:
                    return Blog.objects.filter(tag__title__icontains=tag).distinct()
            else:
                return Blog.objects.filter(
                    Q(title__icontains=query) | Q(content__icontains=query)
                ).distinct()
        return Blog.objects.all()


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogapp/blog_detail.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'content', 'tag', 'cover_image']
    template_name = 'blogapp/blog_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'tag', 'cover_image']
    template_name = 'blogapp/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.pk})
    
    def test_func(self):
        return self.request.user == self.get_object().author


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogapp:blog_list')
    template_name = 'blogapp/blog_confirm_delete.html'

    def test_func(self):
        return self.request.user == self.get_object().author
    
    # Nota: El borrado suave (soft-delete) se maneja mejor en el método delete()
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return redirect(self.get_success_url())