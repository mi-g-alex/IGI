# Generated by Django 5.0.6 on 2024-05-27 20:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0018_alter_employee_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animal',
            name='place',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='animals', related_query_name='animals', to='zoo.place'),
        ),
    ]
