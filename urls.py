from django.conf.urls import url

from django_todopago import views

urlpatterns = [
    url(
        r'^post_payment/(?P<operation_id>.*)$',
        views.PostPaymentView.as_view(),
        name='post_payment',
    ),
]

app_name = 'todopago'
