from django.urls import path
from main.views import *

app_name = "main"

urlpatterns = [
    path("", show_search, name="show_search"),
    path("result", show_detailed_result, name="show_detailed_result"),
    path("info", show_infobox, name="show_infobox"),
    path("player_detail/<str:label>", show_player_detail, name="show_player_detail"),
    path("team_detail/<str:label>", show_team_detail, name="show_team_detail"),
    path("venue_detail/<str:label>", show_venue_detail, name="show_venue_detail"),
]