# Generated by Django 5.0.2 on 2024-07-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_alter_article_content_alter_article_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=1024),
        ),
    ]
