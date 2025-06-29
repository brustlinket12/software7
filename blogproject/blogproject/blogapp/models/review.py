# blog_app/models/review.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Importación local
from .blog import Blog

class ReviewManager(models.Manager):
    """
    Manager para devolver solo las reviews que no están marcadas como eliminadas.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    # Managers
    objects = ReviewManager()
    all_objects = models.Manager()

    class Meta:
        unique_together = ('blog', 'reviewer') # Un usuario solo puede dejar una review por blog

    def __str__(self):
        return f"Review de {self.reviewer.username} en {self.blog.title}"
    
    def save(self, *args, **kwargs):
        """
        Al guardar una nueva review, actualiza el rating promedio del blog.
        """
        super().save(*args, **kwargs)
        self.blog.update_average_rating()

    def delete(self, *args, **kwargs):
        """
        Al eliminar una review (en este caso, un borrado lógico),
        también actualiza el rating del blog.
        """
        # Nota: aquí estás haciendo un borrado físico por defecto (super().delete).
        # Si quisieras hacer un borrado lógico también para las reviews, harías:
        # self.is_deleted = True
        # self.save()
        # Pero mantendré tu lógica original que llama a super().delete()
        # y luego actualiza el blog.
        
        blog_instance = self.blog
        super().delete(*args, **kwargs) # Borrado físico de la BD
        blog_instance.update_average_rating()