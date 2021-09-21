from django.urls import path

from .views import RentalView, EndRentalView, RentalInfoView

app_name = "rental_service"

urlpatterns = [
    path('api/v1/rental', RentalView.as_view()),
    path('api/v1/rental/<uuid:rentalUid>', EndRentalView.as_view()),
    path('api/v1/rental/car/<uuid:rentalUid>', RentalInfoView.as_view()),
]
