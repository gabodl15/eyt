# Generated by Django 4.2.3 on 2023-07-30 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
