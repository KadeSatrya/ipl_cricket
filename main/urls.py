from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_search, name="show_search"),
    path("result/general", show_general_result, name="show_general_result"),
    path("result/detailed", show_detailed_result, name="show_detailed_result"),
    path("info", show_infobox, name="show_infobox")
]