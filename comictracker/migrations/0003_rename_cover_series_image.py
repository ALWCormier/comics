# Generated by Django 4.2.3 on 2024-02-19 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comictracker', '0002_series_cover'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='cover',
            new_name='image',
        ),
    ]