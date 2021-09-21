from django.urls import path

from .views import OfficeView, CarsInOfficeView, CarInAllOfficesView, \
     OfficeCarInfoView, ChangeOfficeStateView, HealthCheckView, OfficeInfoView

app_name = "rentaloffice_service"

urlpatterns = [
    path('api/v1/offices', OfficeView.as_view()),
    path('api/v1/offices/<uuid:officeUid>', OfficeInfoView.as_view()),
    path('api/v1/offices/<uuid:officeUid>/cars', CarsInOfficeView.as_view()),
    path('api/v1/offices/cars/<uuid:carUid>', CarInAllOfficesView.as_view()),
    path('api/v1/offices/<uuid:officeUid>/cars/<uuid:carUid>', OfficeCarInfoView.as_view()),
    path('api/v1/offices/<uuid:officeUid>/car/<uuid:carUid>', ChangeOfficeStateView.as_view()),
    path('api/v1/offices/healthcheck', HealthCheckView.as_view()),
]
