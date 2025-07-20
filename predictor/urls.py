from django.urls import path
from .views import PredictView, prediction_form_view

urlpatterns = [
    path('predict/', PredictView.as_view(), name='predict'),
    path('', prediction_form_view, name='prediction_form'),
]
