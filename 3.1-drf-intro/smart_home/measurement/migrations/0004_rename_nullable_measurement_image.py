# Generated by Django 4.1.3 on 2022-12-22 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0003_measurement_nullable'),
    ]

    operations = [
        migrations.RenameField(
            model_name='measurement',
            old_name='nullable',
            new_name='image',
        ),
    ]
