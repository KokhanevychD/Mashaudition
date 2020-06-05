import os
import pandas
import re
from langdetect import detect
from xlrd import XLRDError
from datetime import datetime

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect

from files.forms import DocumentForm
from player.models import Player
from audit.models import PlayerAudit
from patern.models import PatternBody


class DocumentUpload(CreateView):
    # create PlayerAudit objects from uploaded file
    # after parsing delete file, and instance of DocumentForm
    form_class = DocumentForm
    template_name = 'files/upload.html'
    success_url = reverse_lazy('player:list')

    def form_valid(self, form):
        self.object = form.save()
        try:
            self.parse(self.object.excel)
        except XLRDError:
            os.remove(self.object.excel.path)
            self.object.delete()
            return redirect('files:upload')
        os.remove(self.object.excel.path)
        self.object.delete()
        return redirect('player:list')

    def parse(self, excel):
        # search player nick name from title of PS excel audit file
        # working with RU files

        head = pandas.read_excel(excel, nrows=0, usecols=[0])
        player = head.columns[0]
        lang = detect(player)
        if lang == 'ru':
            player = re.search(r'для (\S+)', player)
            date_format = r'%d.%m.%Y %I:%M %p'
        else:
            player = re.search(r'Audit .(\S+). ', player)
            date_format = r'%Y/%m/%d %I:%M %p'
        player = player.group(1)
        # search for player object
        # if there is now player - create new instance of Player model
        if 'pk' in self.kwargs.keys():
            player_obj = Player.objects.get(pk=self.kwargs['pk'])
            if player_obj.name != player:
                player_obj.name = player_obj.name + ', ' + player
                player_obj.save()
        else:
            player_obj = Player.objects.filter(name=player)
            if len(player_obj) < 1:
                player_obj = Player(name=player)
                player_obj.save()
            else:
                player_obj = player_obj[0]

        # cutin empty colums
        excel_rows = pandas.read_excel(excel, header=2, parse_dates=False)
        excel_rows.dropna(axis=1, how='all', inplace=True)
        excel.close()
        # set list of keys
        columns = excel_rows.columns.values.tolist()
        keys = ['date_played', 'action', 'action_number',
                'game', 'curency', 'summary', 's_coins', 't_money', 'w_money',
                'cashier', 'get_s_coins', 't_money_cashier', 'w_money_cashier',
                ]
        # queryset of patterns
        pattern_query = PatternBody.objects.all()
        # run loop to create PlayerAudit instences,
        # format date to date field and write action type
        for _, row in excel_rows.iterrows():
            kwargs = {}
            for key in range(len(keys)):
                kwargs[keys[key]] = row[columns[key]]
            try:
                kwargs['date_played'] = datetime.strptime(str(kwargs[keys[0]]),
                                                      date_format)
            except ValueError:
                date_format = r'%Y-%m-%d %H:%M:%S'
                kwargs['date_played'] = datetime.strptime(str(kwargs[keys[0]]),
                                                      date_format)
            for item in pattern_query:
                if item.pattern in kwargs['action']:
                    kwargs['action_type'] = item.pattern_type.pattern_name
                    break
            audit = PlayerAudit(player=player_obj, **kwargs)
            audit.save()
