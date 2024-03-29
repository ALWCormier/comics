# Generated by Django 4.2.3 on 2024-02-26 22:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comictracker', '0007_alter_comic_series'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='comic',
            name='cover_artist',
        ),
        migrations.AlterField(
            model_name='comic',
            name='series',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='comictracker.series'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comic',
            name='variant',
            field=models.BooleanField(),
        ),
        migrations.AddField(
            model_name='comic',
            name='artist',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='comictracker.artist'),
            preserve_default=False,
        ),
    ]
