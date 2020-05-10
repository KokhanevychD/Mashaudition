from django.db import models

from player.models import Player


# remaking excel data to model rows
class PlayerAudit(models.Model):
    class Meta:
        ordering = ['date_played']
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

    def __str__(self):
        try:
            return self.player.name
        except Player.DoesNotExist:
            return 'no player'
