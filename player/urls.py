from django.urls import path

from player.views import PlayerList


app_name = 'player'
urlpatterns = [
    path('', PlayerList.as_view(), name='list'),
]