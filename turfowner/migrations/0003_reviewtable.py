# Generated by Django 5.1.2 on 2024-11-12 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turfowner', '0002_alter_turf_table_closed_alter_turf_table_slots'),
    ]

    operations = [
        migrations.CreateModel(
            name='reviewtable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('message', models.TextField()),
            ],
        ),
    ]
