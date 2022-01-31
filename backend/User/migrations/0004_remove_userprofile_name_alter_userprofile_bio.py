# Generated by Django 4.0.1 on 2022-01-31 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_userprofile_bio_userprofile_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='bio',
            field=models.TextField(blank=True, default='Edit this to be your bio.', max_length=500),
        ),
    ]
