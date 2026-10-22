import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EspacoEsportivoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100, verbose_name='nome')),
                ('tipo', models.CharField(choices=[('QUADRA_POLIESPORTIVA', 'Quadra poliesportiva'), ('CAMPO_DE_FUTEBOL', 'Campo de futebol'), ('GINASIO', 'Ginásio'), ('QUADRA_DE_AREIA', 'Quadra de areia'), ('QUADRA_DE_TENIS', 'Quadra de tênis')], max_length=20, verbose_name='tipo')),
                ('capacidade', models.PositiveIntegerField(verbose_name='capacidade')),
                ('ativo', models.BooleanField(default=True, verbose_name='ativo')),
            ],
            options={
                'verbose_name': 'espaço esportivo',
                'verbose_name_plural': 'espaços esportivos',
                'db_table': 'espacos_espaco_esportivo',
                'ordering': ('nome',),
                'constraints': [models.UniqueConstraint(django.db.models.functions.text.Lower('nome'), name='espacos_espaco_esportivo_nome_unico_sem_caixa'), models.CheckConstraint(condition=models.Q(('capacidade__gte', 1)), name='espacos_espaco_esportivo_capacidade_minima'), models.CheckConstraint(condition=models.Q(('tipo__in', ['QUADRA_POLIESPORTIVA', 'CAMPO_DE_FUTEBOL', 'GINASIO', 'QUADRA_DE_AREIA', 'QUADRA_DE_TENIS'])), name='espacos_espaco_esportivo_tipo_valido')],
            },
        ),
    ]
