# Generated by Django 2.2.5 on 2020-02-12 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20200212_1349'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recomendacion',
            name='nivel',
        ),
    ]
