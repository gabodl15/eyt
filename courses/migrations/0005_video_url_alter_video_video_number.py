# Generated by Django 4.2.3 on 2023-08-20 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_video_video_current_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='video_number',
            field=models.IntegerField(),
        ),
    ]