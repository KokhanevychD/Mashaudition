import pandas
import re
from langdetect import detect


from django.db import models

from player.models import Player
from audit.models import PlayerAudit


class Document(models.Model):
    excel = models.FileField(upload_to='uploads')

    def parse(self):
        # search player nick name from title of PS excel audit file
        # working with RU files
        excel = self.excel
        head = pandas.read_excel(excel, nrows=0, usecols=[0])
        player = head.columns[0]
        lang = detect(player)
        if lang == 'ru':
            player = re.search(r'для (\S+)', player)
        else:
            player = re.search(r'Audit .(\S+). ', player)
        player = player.group(1)

        # search for player object
        # if there is now player - create new instance of Player model

        player_obj = Player.objects.filter(name=player)
        if len(player_obj) < 1:
            player_obj = Player(name=player)
            player_obj.save()

        # cutin empty colums
        excel_rows = pandas.read_excel(excel, header=2)
        excel_rows.dropna(axis=1, how='all', inplace=True)
        excel.close()
        # set list of keys
        columns = excel_rows.columns.values.tolist()
        self._audit_fabric(player, columns, excel_rows)

    def _audit_fabric(self, player, columns, excel):
        player = Player.objects.get(name=player)
        for idx, row in excel.iterrows():
            args_list = []
            for key in columns:
                args_list.append(row[key])
            PlayerAudit.create(player, args_list)
