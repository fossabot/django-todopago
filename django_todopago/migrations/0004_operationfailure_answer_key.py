from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todopago', '0003_operationpayment_payment_notnull'),
    ]

    operations = [
        migrations.AddField(
            model_name='operationfailure',
            name='answer_key',
            field=models.CharField(
                default='',
                max_length=40,
                verbose_name='answer_key',
            ),
            preserve_default=False,
        ),
    ]
