# Generated by Django 2.2.5 on 2020-01-25 20:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_remove_respuesta_seccion'),
    ]

    operations = [
        migrations.AddField(
            model_name='dominio',
            name='description',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Usuario'),
        ),
        migrations.AlterField(
            model_name='respuesta',
            name='valor',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='credenciales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
