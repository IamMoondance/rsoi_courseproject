from django.urls import path

from .views import PaymentView, HealthCheckView, PaymentInfoView, \
     RollbackPaymentView

app_name = "payment_service"

urlpatterns = [
    path('api/v1/payment', PaymentView.as_view()),
    path('api/v1/payment/<uuid:paymentUid>', PaymentInfoView.as_view()),
    path('api/v1/payment/health', HealthCheckView.as_view()),
    path('api/v1/payment/rollback/<uuid:paymentUId>', RollbackPaymentView.as_view()),
]
