# Generated by Django 5.0.6 on 2024-05-27 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sensorapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LecturaTemperatura2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('temperatura', models.FloatField()),
            ],
        ),
    ]