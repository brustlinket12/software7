# Generated by Django 5.1.3 on 2025-05-05 02:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0009_tag"),
    ]

    operations = [
        migrations.AddField(
            model_name="blog",
            name="tag",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
