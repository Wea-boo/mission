# Generated by Django 4.1.8 on 2023-04-23 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mission', '0002_alter_customuser_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mission.employee'),
        ),
    ]
