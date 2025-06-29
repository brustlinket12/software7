# blog_app/models/tag.py

from django.db import models

class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"
    