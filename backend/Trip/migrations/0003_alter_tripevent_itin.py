# Generated by Django 4.0.1 on 2022-02-16 08:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Trip', '0002_alter_itinerary_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripevent',
            name='itin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip_event', to='Trip.itinerary'),
        ),
    ]
