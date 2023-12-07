from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_search, name="show_search"),
    path("/result", show_result, name="show_result"),
]