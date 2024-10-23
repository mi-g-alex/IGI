# Generated by Django 5.1.1 on 2024-10-20 10:36

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0023_adsbanners_partners'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutYearHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('year', models.DateField()),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='about',
            name='year_history',
        ),
    ]