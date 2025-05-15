from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from PIL import Image
from django.core.exceptions import ValidationError
from django.db.models import Avg  
from tinymce.models import HTMLField

def dimension_imagen(image): #esta es la funcion para ver q no sea tan grande la imagen
    img = Image.open(image)
    width, height = img.size

    max_width = 300
    max_height = 300

    if width > max_width or height > max_height:
        raise ValidationError(f"Las dimensiones de la imagen no pueden ser mayores a {max_width}x{max_height} píxeles.")

# MODELOS

class BlogManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"

class Blog(models.Model):
    title = models.CharField(max_length=200)
    # content = models.TextField(max_length=2000)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag,on_delete=models.SET_NULL, null=True, max_length=100)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True,validators=[dimension_imagen]) # guarda la imagen en el blog en base y nomas valida el tamano 
    average_rating = models.FloatField(default=0)

    objects = BlogManager()
    all_objects = models.Manager()

    def delete(self, *args  , **kwargs):
        self.is_deleted = True
        self.save()


    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        self.average_rating = self.reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        self.save()

class ReviewManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Review(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

    objects = ReviewManager()
    all_objects = models.Manager()

    class Meta:
        unique_together = ('blog', 'reviewer')

    def __str__(self):
        return f"{self.reviewer.username} - {self.blog.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.blog.update_average_rating()

    def delete(self, *args, **kwargs):
        blog = self.blog
        super().delete(*args, **kwargs)
        blog.update_average_rating()



class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter.username}"