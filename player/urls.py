from django.urls import path

from player.views import PlayerList, PlayerDel, PlayerDetail


app_name = 'player'
urlpatterns = [
    path('', PlayerList.as_view(), name='list'),
    path('del/<int:pk>', PlayerDel.as_view(), name='del-player'),
    path('detail/<int:pk>', PlayerDetail.as_view(), name='detail-player')
]
