# Generated by Django 5.0.2 on 2024-07-15 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0010_article_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='user',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='social_media_links',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]