import django.contrib.postgres.constraints
import django.contrib.postgres.fields.ranges
import reservas.infrastructure.models
from django.contrib.postgres.operations import BtreeGistExtension
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        BtreeGistExtension(),
        migrations.CreateModel(
            name='ReservaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('espaco_id', models.BigIntegerField(verbose_name='espaço')),
                ('solicitante_usuario_id', models.BigIntegerField(db_index=True, verbose_name='usuário solicitante')),
                ('solicitante_nome', models.CharField(max_length=150, verbose_name='nome do solicitante')),
                ('solicitante_matricula', models.CharField(max_length=20, verbose_name='matrícula do solicitante')),
                ('inicio', models.DateTimeField(verbose_name='início')),
                ('fim', models.DateTimeField(verbose_name='fim')),
                ('finalidade', models.CharField(max_length=200, verbose_name='finalidade')),
                ('situacao', models.CharField(choices=[('SOLICITADA', 'Solicitada'), ('CONFIRMADA', 'Confirmada'), ('RECUSADA', 'Recusada'), ('CANCELADA', 'Cancelada'), ('CONCLUIDA', 'Concluída')], max_length=10, verbose_name='situação')),
                ('motivo_da_situacao', models.CharField(blank=True, default='', max_length=300, verbose_name='motivo da situação')),
                ('criada_em', models.DateTimeField(verbose_name='criada em')),
            ],
            options={
                'verbose_name': 'reserva',
                'verbose_name_plural': 'reservas',
                'db_table': 'reservas_reserva',
                'ordering': ('inicio', 'id'),
                'indexes': [models.Index(fields=['espaco_id', 'inicio'], name='reservas_espaco_inicio_idx')],
                'constraints': [models.CheckConstraint(condition=models.Q(('fim__gt', models.F('inicio'))), name='reservas_reserva_fim_apos_inicio'), models.CheckConstraint(condition=models.Q(('situacao__in', ['SOLICITADA', 'CONFIRMADA', 'RECUSADA', 'CANCELADA', 'CONCLUIDA'])), name='reservas_reserva_situacao_valida'), models.CheckConstraint(condition=models.Q(models.Q(('situacao__in', ['CANCELADA', 'RECUSADA']), _negated=True), models.Q(('motivo_da_situacao', ''), _negated=True), _connector='OR'), name='reservas_reserva_motivo_obrigatorio'), django.contrib.postgres.constraints.ExclusionConstraint(condition=models.Q(('situacao__in', ['CONFIRMADA', 'SOLICITADA'])), expressions=((reservas.infrastructure.models.TsTzRange('inicio', 'fim', django.contrib.postgres.fields.ranges.RangeBoundary(inclusive_lower=True, inclusive_upper=False)), '&&'), ('espaco_id', '=')), name='reservas_reserva_sem_sobreposicao_no_espaco')],
            },
        ),
    ]
