from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=50)

    def uniq_actions(self):
        queryset = self.audit.all()
        actions = {}
        for row in queryset:
            if row.action in actions.keys():
                actions[row.action]['number'] += 1
                actions[row.action]['row'].append(row)
            else:
                actions[row.action] = {}
                actions[row.action]['number'] = 1
                actions[row.action]['row'] = [row, ]
        return actions

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        obj = cls(name=name)
        obj.save()
        return obj
