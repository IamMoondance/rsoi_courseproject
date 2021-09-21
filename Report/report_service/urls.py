from django.urls import path

from .views import BookingModelView, BookingOfficesView

app_name = "report_service"

urlpatterns = [
    path('api/v1/reports/booking-by-models', BookingModelView.as_view()),
    path('api/v1/reports/booking-by-offices', BookingOfficesView.as_view()),
]
