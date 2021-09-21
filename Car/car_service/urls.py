from django.urls import path

from .views import CarsView, CarView, HealthCheckView

app_name = "car_service"

urlpatterns = [
    path('api/v1/cars', CarsView.as_view()),
    path('api/v1/cars/<uuid:carUid>', CarView.as_view()),
    path('api/v1/cars/healthcheck', HealthCheckView.as_view())
]
