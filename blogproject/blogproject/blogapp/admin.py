from django.contrib import admin
from .models import Blog, Review, Comment

class BlogAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Blog.all_objects.all()


admin.site.register(Blog, BlogAdmin)
admin.site.register(Review)
admin.site.register(Comment)