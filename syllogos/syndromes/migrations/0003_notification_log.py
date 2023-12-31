# Generated by Django 2.2.17 on 2021-06-07 13:20

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('syndromes', '0002_registar_actions'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=1024)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('description', models.CharField(default='email', max_length=256, null=True)),
                ('registar', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='syndromes.Registar')),
            ],
        ),
    ]
