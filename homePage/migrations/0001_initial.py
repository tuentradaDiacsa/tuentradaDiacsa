# Generated by Django 4.2.1 on 2023-06-07 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaHora', models.DateTimeField()),
                ('celular', models.PositiveIntegerField()),
                ('recibo', models.PositiveBigIntegerField()),
                ('cip', models.PositiveIntegerField()),
                ('pin', models.PositiveIntegerField()),
                ('monto', models.PositiveBigIntegerField()),
                ('confirmado', models.DateTimeField(blank=True, null=True)),
                ('sms', models.BooleanField()),
                ('nombre', models.TextField(blank=True, max_length=40, null=True)),
                ('correo', models.TextField(blank=True, max_length=50, null=True)),
                ('dni', models.PositiveIntegerField(blank=True, null=True)),
                ('pregunta1', models.TextField(blank=True, max_length=50, null=True)),
                ('pregunta2', models.TextField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preguntas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveIntegerField()),
                ('pregunta', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket', models.PositiveIntegerField()),
                ('cip', models.PositiveIntegerField()),
                ('tipo', models.PositiveIntegerField()),
                ('fechaHora', models.DateTimeField()),
                ('celular', models.PositiveIntegerField()),
                ('recibo', models.PositiveIntegerField()),
                ('pinIntentos', models.PositiveIntegerField()),
                ('confirmado', models.DateTimeField(blank=True, null=True)),
                ('nombre', models.TextField(blank=True, max_length=40, null=True)),
                ('correo', models.TextField(blank=True, max_length=50, null=True)),
                ('dni', models.PositiveIntegerField(blank=True, null=True)),
                ('pregunta1', models.TextField(blank=True, max_length=50, null=True)),
                ('pregunta2', models.TextField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.PositiveIntegerField()),
                ('descripcion', models.TextField()),
                ('precio', models.PositiveIntegerField()),
                ('cantidad', models.PositiveBigIntegerField(default=100)),
            ],
        ),
    ]
