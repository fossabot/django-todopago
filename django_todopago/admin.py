from django.contrib import admin
from django.db.models import F
from django.utils.translation import ugettext_lazy as _

from django_todopago import models


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'merchant_id',
        'sandbox',
    )


class OperationPaymentInline(admin.StackedInline):
    model = models.OperationPayment
    extra = 0

    readonly_fields = (
        'answer_key',
        'payment_date',
    )

    def has_add_permission(self, request=None, obj=None):
        return False


class OperationFailureInline(admin.StackedInline):
    model = models.OperationFailure
    extra = 0

    readonly_fields = (
        'answer_key',
        'code',
        'message',
        'failure_date',
    )

    def has_add_permission(self, request=None, obj=None):
        return False


@admin.register(models.Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'merchant_name',
        'operation_id',
        'is_paid',
    )
    readonly_fields = (
        'payment_url',
        'request_key',
        'public_request_key',
    )
    inlines = (
        OperationPaymentInline,
        OperationFailureInline,
    )

    def merchant_name(self, obj):
        return obj.merchant.name
    merchant_name.short_description = _('Merchant name')
    merchant_name.admin_order_field = 'merchant_id'

    def is_paid(self, obj):
        return obj.is_paid is not None
    is_paid.boolean = True
    is_paid.short_description = _('Paid')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'merchant',
        ).annotate(
            is_paid=F('payment__pk'),
        )
