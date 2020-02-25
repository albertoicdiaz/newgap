# Generated by Django 2.2.5 on 2020-02-22 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_remove_recomendacion_nivel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='tipo_usuario',
        ),
        migrations.AddField(
            model_name='cargo',
            name='tipo_usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users.TipoUsuario'),
            preserve_default=False,
        ),
    ]