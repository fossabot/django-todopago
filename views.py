from django.conf import settings
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from django_todopago import models


class PostPaymentView(View):

    def get(self, request, operation_id):
        answer_key = request.GET.get('Answer')
        operation = models.Operation.objects.get(operation_id=operation_id)
        operation.process_answer(answer_key)

        return redirect(settings.TODOPAGO_POST_PAYMENT_VIEW, operation.pk)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
