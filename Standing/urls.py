from Standing.views import *
from django.urls import path

urlpatterns = [
    path('<int:year>/', CurrentStandingGraphView.as_view(), name="standing"),
]
