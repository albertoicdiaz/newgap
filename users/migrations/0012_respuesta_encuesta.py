# Generated by Django 2.2.5 on 2020-01-29 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_encuesta_realizar_enc'),
    ]

    operations = [
        migrations.AddField(
            model_name='respuesta',
            name='encuesta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.Encuesta'),
            preserve_default=False,
        ),
    ]