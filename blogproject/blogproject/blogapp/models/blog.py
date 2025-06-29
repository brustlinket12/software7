# blog_app/models/blog.py

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Avg
from PIL import Image
from tinymce.models import HTMLField

# Importación local desde otro archivo de modelo
from .tag import Tag

def dimension_imagen(image):
    """
    Valida que las dimensiones de la imagen no excedan un máximo.
    """
    try:
        img = Image.open(image)
        width, height = img.size
        max_width = 300
        max_height = 300

        if width > max_width or height > max_height:
            raise ValidationError(
                f"Las dimensiones de la imagen no pueden ser mayores a {max_width}x{max_height} píxeles."
            )
    except FileNotFoundError:
        # Si el archivo no existe (por ejemplo, al limpiar el campo), no se puede validar.
        pass
    except Exception as e:
        # Captura otros posibles errores de PIL
        raise ValidationError(f"Error al procesar la imagen: {e}")


class BlogManager(models.Manager):
    """
    Manager para devolver solo los blogs que no están marcados como eliminados.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, blank=True)
    cover_image = models.ImageField(
        upload_to='covers/', 
        blank=True, 
        null=True,
        validators=[dimension_imagen]
    )
    average_rating = models.FloatField(default=0)

    # Managers
    objects = BlogManager()      # Muestra solo los activos: Blog.objects.all()
    all_objects = models.Manager() # Muestra todos: Blog.all_objects.all()

    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método delete para hacer un borrado lógico (soft delete).
        """
        self.is_deleted = True
        self.save()

    def __str__(self):
        return self.title
    
    def update_average_rating(self):
        """
        Calcula y actualiza el rating promedio basado en sus 'reviews' activas.
        Usamos 'self.reviews' que es el related_name definido en el modelo Review.
        """
        # Se asegura de filtrar también las reviews no eliminadas para el cálculo
        avg_rating = self.reviews.filter(is_deleted=False).aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg_rating or 0
        self.save(update_fields=['average_rating'])