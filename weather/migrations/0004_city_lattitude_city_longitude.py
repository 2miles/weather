# Generated by Django 4.0.4 on 2022-06-04 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0003_remove_city_lattitude_remove_city_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='lattitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
