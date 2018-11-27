import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Merchant',
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
                (
                    'name',
                    models.CharField(
                        help_text='A friendly name to recognize this account.',
                        max_length=32,
                        verbose_name='name',
                    )
                ),
                (
                    'merchant_id',
                    models.IntegerField(
                        help_text='The merchant ID given by TodoPago.',
                        verbose_name='merchant id',
                    )
                ),
                (
                    'api_key',
                    models.CharField(
                        help_text='The API key given by TodoPago.',
                        max_length=41,
                        verbose_name='api key',
                    )
                ),
                (
                    'sandbox',
                    models.BooleanField(
                        default=True,
                        help_text=(
                            'Indicates if this account uses the sandbox mode,'
                            ' intended for testing rather than real'
                            ' transactions.'
                        ),
                        verbose_name='sandbox',
                    )
                ),
                (
                    'city',
                    models.CharField(
                        help_text='The city where invoices are emitted',
                        max_length=50,
                        verbose_name='city',
                    )
                ),
                (
                    'country',
                    models.CharField(
                        help_text=(
                            'The country code where invoices are emitted',
                        ),
                        max_length=2,
                        verbose_name='country',
                    )
                ),
                (
                    'post_code',
                    models.CharField(
                        help_text='The post code where invoices are  emitted',
                        max_length=10,
                        verbose_name='post code',
                    )
                ),
                (
                    'province',
                    models.CharField(
                        help_text='The province where invoices are emitted',
                        max_length=2,
                        verbose_name='province',
                    )
                ),
                (
                    'address',
                    models.CharField(
                        help_text='The address where invoices emitted',
                        max_length=60,
                        verbose_name='address',
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
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
                (
                    'operation_id',
                    models.CharField(
                        max_length=40,
                        unique=True,
                        verbose_name='operation id',
                    )
                ),
                ('payment_url', models.URLField(verbose_name='payment url')),
                (
                    'request_key',
                    models.CharField(
                        max_length=48,
                        verbose_name='request key',
                    )
                ),
                (
                    'public_request_key',
                    models.CharField(
                        max_length=48,
                        verbose_name='public request key',
                    )
                ),
                (
                    'merchant',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='operations',
                        to='todopago.Merchant',
                        verbose_name='merchant',
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='OperationPayment',
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
                (
                    'answer_key',
                    models.CharField(
                        max_length=40,
                        verbose_name='answer_key',
                    )
                ),
                (
                    'payment_date',
                    models.DateTimeField(
                        null=True,
                        verbose_name='payment date',
                    )
                ),
                (
                    'operation',
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name='payment',
                        to='todopago.Operation',
                        verbose_name='merchant',
                    )
                ),
            ],
        ),
    ]
