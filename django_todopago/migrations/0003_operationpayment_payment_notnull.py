from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todopago', '0002_operationfailure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationpayment',
            name='payment_date',
            field=models.DateTimeField(verbose_name='payment date'),
        ),
    ]
