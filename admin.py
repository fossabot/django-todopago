from django.contrib import admin

from django_todopago import models


@admin.register(models.Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'merchant_id'
    )
