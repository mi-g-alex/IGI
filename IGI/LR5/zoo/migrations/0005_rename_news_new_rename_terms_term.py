# Generated by Django 5.0.6 on 2024-05-25 11:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('zoo', '0004_news_price_promo_terms_ticket_user_comment_vacancy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='News',
            new_name='New',
        ),
        migrations.RenameModel(
            old_name='Terms',
            new_name='Term',
        ),
    ]