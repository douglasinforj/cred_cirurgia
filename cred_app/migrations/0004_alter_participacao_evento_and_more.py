# Generated by Django 5.1.2 on 2025-02-10 04:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cred_app', '0003_alter_participante_cnpj_empresa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participacao',
            name='evento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cred_app.evento'),
        ),
        migrations.AlterField(
            model_name='participacao',
            name='participante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='cred_app.participante'),
        ),
    ]
