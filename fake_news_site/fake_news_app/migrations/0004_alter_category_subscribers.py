# Generated by Django 5.0.3 on 2024-03-23 16:16

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fake_news_app', '0003_category_subscribers'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='categories', to=settings.AUTH_USER_MODEL),
        ),
    ]