from django.contrib import admin
from .models import Blog, Tag, Review, Comment
from tinymce.widgets import TinyMCE
from django import forms
from django.db import models
from django.utils.html import format_html

admin.site.site_header = "Rate.it Admin Portal"
admin.site.site_title = "Rate.it Admin"

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    #limitar rating a 1 a 5
    formfield_overrides = {
        models.IntegerField: {'widget': forms.NumberInput(attrs={'min': 1, 'max': 5})},
    }

#visualización de todo el contenido de los blogs
class BlogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Blog.all_objects.all()
    
    list_display = ('title', 'author', 'created_at', 'cantidad_reviews', 'is_deleted', 'color_rating')
    list_display_links = ('title', 'author')
    list_editable = ('is_deleted',)
    list_filter = ('is_deleted', 'author', 'tag', 'created_at')

    search_fields = ('title__startswith', 'tag')
    ordering = ('-title', '-author', '-created_at',)

    readonly_fields = ('created_at', 'image_preview',)
    list_per_page = 10

    inlines = (ReviewInline,) #muestra el campo de las reviews dentro de los blogs

    #colores en rating
    @admin.display(description='Average Rating', ordering='-average_rating',)
    def color_rating(self, obj):
        if obj.average_rating >= 4:
            color = 'orange'
        elif obj.average_rating >= 2:
            color = 'skyblue'
        else:
            color = 'gray'
        return format_html('<span style="color: {};">{}</span>', color, obj.average_rating)

    #cuenta las reviews para mostrar en el admin
    def cantidad_reviews(self, obj):
        return obj.reviews.count()
    
    #carga una preview de la imagen del blog
    def image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.cover_image.url)
        return "Sin imagen"



# visualizacion de las vainas dentro de review, igual q arriba
class ReviewAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Review.all_objects.all()
    
    list_display = ('blog', 'reviewer', 'created_at', 'is_deleted', 'color_rating')
    list_display_links = ('blog', 'reviewer')
    list_editable = ('is_deleted',)
    list_filter = ('is_deleted', 'blog', 'reviewer', 'created_at')

    search_fields = ('blog__title__startswith', 'reviewer__username')
    ordering = ('-blog', '-reviewer', '-created_at',)

    readonly_fields = ('created_at',)
    list_per_page = 10

    #colores para el rating
    @admin.display(description='Rating', ordering='-rating',)
    def color_rating(self, obj):
        if obj.rating >= 4:
            color = 'orange'
        elif obj.rating >= 2:
            color = 'skyblue'
        else:
            color = 'gray'
        return format_html('<span style="color: {};">{}</span>', color, obj.rating)



admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment)