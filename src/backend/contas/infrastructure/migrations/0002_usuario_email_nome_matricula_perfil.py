import django.db.models.functions.text
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='usuario',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='username',
        ),
        migrations.AddField(
            model_name='usuario',
            name='matricula',
            field=models.CharField(default='', error_messages={'unique': 'Já existe um usuário com esta matrícula.'}, max_length=20, unique=True, verbose_name='matrícula'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='nome',
            field=models.CharField(default='', max_length=150, verbose_name='nome'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='perfil',
            field=models.CharField(choices=[('SOLICITANTE', 'Solicitante'), ('GESTOR', 'Gestor')], default='SOLICITANTE', max_length=20, verbose_name='perfil'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Já existe um usuário com este e-mail.'}, max_length=254, unique=True, verbose_name='e-mail'),
        ),
        migrations.AddConstraint(
            model_name='usuario',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('email'), name='contas_usuario_email_unico_sem_caixa', violation_error_message='Já existe um usuário com este e-mail.'),
        ),
    ]
