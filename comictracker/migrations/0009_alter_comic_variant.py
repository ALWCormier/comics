# Generated by Django 4.2.3 on 2024-02-27 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comictracker', '0008_artist_remove_comic_cover_artist_alter_comic_series_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='variant',
            field=models.BooleanField(default=False),
        ),
    ]
