# Generated by Django 5.1.3 on 2025-05-01 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0004_alter_blog_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="is_deleted",
            field=models.BooleanField(default=False),
        ),
    ]
