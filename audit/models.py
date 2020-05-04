from datetime import datetime
from django.db import models

from player.models import Player
from patern.models import PatternBody


# remaking excel data to model rows
class PlayerAudit(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,
                               related_name='audit')
    date_played = models.DateTimeField()
    action = models.CharField(max_length=255)
    action_number = models.BigIntegerField()
    game = models.CharField(max_length=255)
    curency = models.CharField(max_length=5)
    summary = models.FloatField()
    s_coins = models.IntegerField()
    t_money = models.FloatField()
    w_money = models.FloatField()
    cashier = models.FloatField()
    get_s_coins = models.IntegerField()
    t_money_cashier = models.FloatField()
    w_money_cashier = models.FloatField()
    action_type = models.CharField(max_length=20, blank=True, null=True)

    @classmethod
    def create(cls, player, args_list):
        # asign values to keys, which are PlayerAudit fields
        keys = ['date_played', 'action', 'action_number',
                'game', 'curency', 'summary', 's_coins', 't_money', 'w_money',
                'cashier', 'get_s_coins', 't_money_cashier', 'w_money_cashier',
                ]
        kwargs = {}
        for idx in range(len(keys)):
            kwargs[keys[idx]] = args_list[idx]
        pattern_query = PatternBody.objects.all()
        for item in pattern_query:
            if item.pattern in kwargs['action']:
                kwargs['action_type'] = item.pattern_type.pattern_name
                break
        date_format = '%d.%m.%Y %I:%M %p'
        kwargs['date_played'] = datetime.strptime(kwargs[keys[0]], date_format)
        audit_row = cls(player=player, **kwargs)
        audit_row.save()

    def __str__(self):
        try:
            return self.player.name
        except Player.DoesNotExist:
            return 'no player'
