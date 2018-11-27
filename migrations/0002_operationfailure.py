import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todopago', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationFailure',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                ('code', models.PositiveIntegerField(verbose_name='code',)),
                (
                    'message',
                    models.CharField(
                        max_length=256,
                        verbose_name='message',
                    )
                ),
                (
                    'failure_date',
                    models.DateTimeField(
                        null=True,
                        verbose_name='payment date',
                    )
                ),
                (
                    'operation',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='failure',
                        to='todopago.Operation',
                        verbose_name='merchant',
                    )
                ),
            ],
        ),
    ]
