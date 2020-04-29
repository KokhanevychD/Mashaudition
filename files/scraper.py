import pandas
import re

from files.models import PlayerAudit
from player.models import Player


def scraper(excel):
    # search player nick name from title of PS excel audit file
    # working with RU files
    head = pandas.read_excel(excel, nrows=0, usecols=[0])
    for column in head.columns:
        player = str(column)
    player = re.search(r'для (\S+)', player)
    player = player.group(1)

    # search for player
    # if there is now player - create new instance of Player model
    player_obj = Player.objects.filter(name=player)
    if len(player_obj) < 1:
        player_obj = Player.create(player)

    excel = pandas.read_excel(excel, header=2)
    print(excel)
    # for i, r in excel.iterrows():
    #     print(r['Действие'])
