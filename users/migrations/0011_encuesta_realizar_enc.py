# Generated by Django 2.2.5 on 2020-01-29 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200127_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('fecha_termino', models.DateField()),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Trabajador')),
            ],
        ),
        migrations.CreateModel(
            name='Realizar_enc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Trabajador')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Encuesta')),
            ],
        ),
    ]