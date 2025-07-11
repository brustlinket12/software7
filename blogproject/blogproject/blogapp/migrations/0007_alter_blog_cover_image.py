# Generated by Django 5.1.3 on 2025-05-02 20:38

import blogapp.models
from django.db import migrations, models
from blogapp.models.blog import dimension_imagen

class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0006_blog_cover_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="cover_image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="covers/",
                validators=[dimension_imagen],
            ),
        ),
    ]
