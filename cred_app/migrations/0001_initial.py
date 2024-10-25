# Generated by Django 5.1.2 on 2024-10-23 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome do Evento')),
                ('data', models.DateTimeField(verbose_name='Data de Início')),
                ('data_termino', models.DateTimeField(blank=True, null=True, verbose_name='Data de Término')),
                ('local', models.CharField(max_length=255, verbose_name='Local do Evento')),
                ('descricao', models.TextField(verbose_name='Descrição do Evento')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/eventos/', verbose_name='Foto do Evento')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='Participante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('cpf', models.CharField(max_length=11, unique=True)),
                ('nome_empresa', models.CharField(max_length=100)),
                ('cnpj_empresa', models.CharField(max_length=14)),
                ('telefone', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name': 'Participante',
                'verbose_name_plural': 'Participantes',
            },
        ),
        migrations.CreateModel(
            name='Participacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inscricao', models.DateTimeField(auto_now_add=True)),
                ('pagamento_confirmado', models.BooleanField(default=False)),
                ('checkin_realizado', models.BooleanField(default=False)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cred_app.evento')),
                ('participante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cred_app.participante')),
            ],
            options={
                'verbose_name': 'Participação',
                'verbose_name_plural': 'Participações',
            },
        ),
    ]
