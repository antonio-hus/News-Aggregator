# Generated by Django 5.0.2 on 2024-07-13 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_alter_article_last_updated_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='last_updated_date',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='article',
            name='publish_date',
            field=models.CharField(max_length=64),
        ),
    ]
