# blog_app/models/comment.py

from django.db import models
from django.contrib.auth.models import User

# Importación local
from .review import Review

class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.commenter.username} en la review #{self.review.id}"