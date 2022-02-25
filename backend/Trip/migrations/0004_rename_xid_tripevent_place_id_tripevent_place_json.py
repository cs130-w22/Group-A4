# Generated by Django 4.0.1 on 2022-02-24 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Trip', '0003_alter_tripevent_itin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tripevent',
            old_name='xid',
            new_name='place_id',
        ),
        migrations.AddField(
            model_name='tripevent',
            name='place_json',
            field=models.TextField(default='default_place_json'),
            preserve_default=False,
        ),
    ]