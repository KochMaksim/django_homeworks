from django.urls import path

from .views import SensorAPI, MeasurementAPI, SensorAPIPatch

urlpatterns = [
    path('sensors/', SensorAPI.as_view()),
    path('sensors/<int:pk>/', SensorAPIPatch.as_view()),
    path('measurement/', MeasurementAPI.as_view()),
]
