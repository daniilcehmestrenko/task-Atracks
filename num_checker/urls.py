from django.urls import path

from .views import GetInfoNumberAPIView, StartDatabaseFilling, check_number


urlpatterns = [
    path('api-check-num/', GetInfoNumberAPIView.as_view(), name='update'),
    path('check_num/', check_number, name='check_number'),
    path('start_filling/', StartDatabaseFilling.as_view(), name='start_filling'),
]
