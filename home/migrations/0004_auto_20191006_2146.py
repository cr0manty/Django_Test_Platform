# Generated by Django 2.2.6 on 2019-10-06 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20191006_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tests',
            field=models.ManyToManyField(blank=True, related_name='user', to='tests.Test'),
        ),
    ]
