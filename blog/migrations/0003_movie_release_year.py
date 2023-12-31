# Generated by Django 4.2.8 on 2023-12-27 11:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_movie_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='release_year',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)]),
            preserve_default=False,
        ),
    ]
