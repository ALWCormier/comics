# Generated by Django 4.2.3 on 2024-02-19 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comictracker', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='cover',
            field=models.URLField(max_length=300, null=True),
        ),
    ]
