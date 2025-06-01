from django.urls import path
from Circuit.views import *

urlpatterns = [
    path("<int:year>/", CircuitView.as_view(), name="circuit"),
]
