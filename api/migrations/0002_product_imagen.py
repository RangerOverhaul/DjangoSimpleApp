# Generated by Django 5.0.4 on 2024-04-23 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]