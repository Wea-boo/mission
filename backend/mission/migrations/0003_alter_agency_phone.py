# Generated by Django 4.1.8 on 2023-04-27 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0002_agency_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='phone',
            field=models.CharField(max_length=12),
        ),
    ]
