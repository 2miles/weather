# Generated by Django 4.0.4 on 2022-05-30 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0002_city_country_city_lattitude_city_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='lattitude',
        ),
        migrations.RemoveField(
            model_name='city',
            name='longitude',
        ),
    ]
