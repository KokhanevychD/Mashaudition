from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        obj = cls(name=name)
        obj.save()
        return obj

    def filter_data(self):
        queryset = self.audit.all()
        transfer_keys = ['Деньги получены', 'Деньги отправлены']
        rake_back = ['Награда из подарка', 'the Deal']
        income_tnmt_keys = ['Победа в турнире',
                            'Промежуточная выплата',
                            'Турнир отменен',
                            'Награда', 'приз', 'Компенсация']
        for row in queryset:
            row.action_type = 'tournaments'
            for pattern in transfer_keys:
                if pattern in row.action:
                    row.action_type = 'transfer'
            for pattern in rake_back:
                if pattern in row.action:
                    row.action_type = 'rb'
            for pattern in income_tnmt_keys:
                if pattern in row.action and not row.action_type:
                    row.action_type = 'income tournaments'
            row.save()
