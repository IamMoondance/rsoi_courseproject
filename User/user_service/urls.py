from django.urls import path

from .views import SessionAuthView, SessionValidateView, InitDBView

app_name = "session_service"

urlpatterns = [
    path('api/v1/session/authorize', SessionAuthView.as_view()),
    path('api/v1/session/validate', SessionValidateView.as_view()),
    path('api/v1/session/init_database', InitDBView.as_view())
]
