# Generated by Django 3.0.5 on 2020-05-17 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
