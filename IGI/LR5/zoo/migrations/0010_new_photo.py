# Generated by Django 5.0.6 on 2024-05-26 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0009_employee_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='photo',
            field=models.ImageField(default=None, null=True, upload_to='photos/news/'),
        ),
    ]
