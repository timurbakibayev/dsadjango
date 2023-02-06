# Generated by Django 4.1.3 on 2022-12-26 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('available', models.IntegerField(default=0)),
                ('image', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
    ]
