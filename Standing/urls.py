from Standing.views import *
from django.urls import path

urlpatterns = [
    path('<int:year>/', CurrentStandingView.as_view(), name="standing"),
]
