# Generated by Django 5.1.1 on 2024-09-17 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0019_alter_animal_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='paid',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
