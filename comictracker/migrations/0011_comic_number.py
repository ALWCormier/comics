# Generated by Django 4.2.3 on 2024-02-27 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comictracker', '0010_alter_comic_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='number',
            field=models.IntegerField(default=1000),
        ),
    ]