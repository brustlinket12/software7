from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseForbidden

from ..models import Blog, Review

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        if Review.objects.filter(blog=self.blog, reviewer=request.user).exists():
            messages.error(self.request, 'Ya has dejado una reseña para esta publicación.')
            return redirect('blogapp:blog_detail', pk=self.blog.pk)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.reviewer = self.request.user
        form.instance.blog = self.blog
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.kwargs['pk']})


class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    fields = ['rating', 'comment']
    template_name = 'blogapp/review_form.html'
    pk_url_kwarg = 'review_pk' # Especifica que el PK de la URL es 'review_pk'

    def get_success_url(self):
        return reverse_lazy('blogapp:blog_detail', kwargs={'pk': self.object.blog.pk})

    def test_func(self):
        return self.request.user == self.get_object().reviewer


def delete_review(request, blog_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk, blog_id=blog_pk)
    if request.user == review.reviewer:
        review.is_deleted = True
        review.save()
        messages.success(request, 'Reseña eliminada correctamente.')
        return redirect('blogapp:blog_detail', pk=blog_pk)
    else:
        return HttpResponseForbidden("No tienes permiso para eliminar esta reseña.")