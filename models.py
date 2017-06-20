import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _


from django_todopago.sdk.todopagoconnector import TodoPagoConnector

logger = logging.getLogger(__name__)


class Merchant(models.Model):
    """A todopago merchant account"""
    name = models.CharField(
        _('name'),
        max_length=32,
        help_text=_('A friendly name to recognize this account.'),
    )
    merchant_id = models.IntegerField(
        _('merchant id'),
        help_text=_('The merchant ID given by TodoPago.'),
    )
    api_key = models.CharField(
        _('api key'),
        max_length=41,
        help_text=_('The API key given by TodoPago.'),
    )
    sandbox = models.BooleanField(
        _('sandbox'),
        default=True,
        help_text=_(
            'Indicates if this account uses the sandbox mode, '
            'intended for testing rather than real transactions.'
        ),
    )
    city = models.CharField(
        _('city'),
        max_length=50,
        help_text=_('The city where invoices are  emitted'),
    )
    country = models.CharField(
        _('country'),
        max_length=2,
        help_text=_('The country code where invoices are  emitted'),
    )
    post_code = models.CharField(
        _('post code'),
        max_length=10,
        help_text=_('The post code where invoices are  emitted'),
    )
    province = models.CharField(
        _('province'),
        max_length=2,
        help_text=_('The province where invoices are emitted'),
    )
    address = models.CharField(
        _('address'),
        max_length=60,
        help_text=_('The address where invoices emitted'),
    )

    @property
    def environment_name(self):
        if self.sandbox:
            return 'test'
        return 'prod'

    @property
    def client(self):
        return TodoPagoConnector(
            {'Authorization': self.api_key},
            self.environment_name,
        )


class OperationManager(models.Manager):

    def create_upstream(
        self,
        merchant,
        operation_id,
        total_amount,
        client_email,
        fraud_control_fields,
        host=settings.TODOPAGO_BASE_HOST,
    ):
        """
        Creates a new Operation and pushes it upstream
        """
        operation_data = {
            'MERCHANT': str(merchant.merchant_id),
            'OPERATIONID': operation_id,
            'CURRENCYCODE': '32',
            'AMOUNT': str(total_amount),
            'EMAILCLIENTE': client_email,
        }
        fraud_control_fields.update({
            'CSBTPOSTALCODE': merchant.post_code,
            'CSBTSTATE': merchant.province,
            'CSBTCITY': merchant.city,
            'CSBTCOUNTRY': 'AR',
        })
        operation_data.update(**fraud_control_fields)

        response = merchant.client.sendAuthorizeRequest(
            {
                "Security": merchant.api_key,
                "URL_OK": host + reverse(
                    'todopago:post_payment',
                    args=(operation_id,)
                ),
                "URL_ERROR": host + reverse(
                    'todopago:post_payment',  # XXX: Should be different?
                    args=(operation_id,)
                )
            },
            operation_data,
        )

        logger.info('Generated TodoPago operation: %s', response)
        if response.StatusCode != -1:
            raise Exception(response.StatusMessage)

        operation = Operation.objects.create(
            merchant=merchant,
            operation_id=operation_id,
            payment_url=response.URL_Request,
            request_key=response.RequestKey,
            public_request_key=response.PublicRequestKey,
        )

        return operation


class Operation(models.Model):
    merchant = models.ForeignKey(
        Merchant,
        verbose_name=_('merchant'),
        related_name='operations',
        on_delete=models.PROTECT,
    )
    operation_id = models.CharField(
        'operation id',
        max_length=40,
        unique=True,
    )
    payment_url = models.URLField(
        'payment url',
    )
    request_key = models.CharField(
        'request key',
        max_length=48,
    )
    public_request_key = models.CharField(
        'public request key',
        max_length=48,
    )

    objects = OperationManager()

    def process_answer(self, answer_key):
        payment, _created = OperationPayment.objects.get_or_create(
            operation=self,
            answer_key=answer_key,
        )

        response = self.merchant.client.getAuthorizeAnswer({
            'Security': self.merchant.api_key,
            'Merchant': str(self.merchant.merchant_id),
            'RequestKey': self.request_key,
            'AnswerKey': answer_key,
        })

        if response.StatusCode == -1:
            payment.payment_date = response.Payload.Answer.DATETIME
            payment.save()
        else:
            logger.info('Generated TodoPago operation: %s', response)
            logger.error(
                'Got an answer for a rejected payment: %s', response
            )


class OperationPayment(models.Model):
    operation = models.OneToOneField(
        Operation,
        verbose_name=_('merchant'),
        related_name='payment',
        on_delete=models.PROTECT,
    )
    answer_key = models.CharField(
        'answer_key',
        max_length=40,
    )
    payment_date = models.DateTimeField(
        _('payment date'),
        null=True,
    )