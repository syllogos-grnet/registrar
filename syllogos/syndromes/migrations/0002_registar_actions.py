# Generated by Django 2.2.17 on 2020-12-08 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('syndromes', '0001_intial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registar',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
