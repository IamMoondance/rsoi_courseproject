from django.urls import path

from .views import IndexView, OfficeListView, CarListView, RentalView, \
    SignInView, SignUpView, OfficeInfoView, OfficeCarInfoView, RentalChangeView

app_name = "gateway_service"

urlpatterns = [
    path('', IndexView.as_view()),
    path('signin', SignInView.as_view()),
    path('signup', SignUpView.as_view()),
    path('offices', OfficeListView.as_view()),
    path('offices/<uuid:officeUid>', OfficeInfoView.as_view()),
    path('cars', CarListView.as_view()),
    path('cars/<uuid:officeUid>', OfficeCarInfoView.as_view()),
    path('rental', RentalView.as_view()),
    path('rental/<uuid:rentalUid>', RentalChangeView.as_view()),
]