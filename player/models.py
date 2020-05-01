from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=50)

    def uniq_actions(self):
        queryset = self.audit.all()
        actions = {}
        for row in queryset:
            if row.action in actions.keys():
                actions[row.action].append(row)
            else:
                actions[row.action] = [row, ]
        return actions

    def uniq_game_type(self):
        pass

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        obj = cls(name=name)
        obj.save()
        return obj

# TODO actions list:
# Регистрация в турнире
# Награда: приз за выбивание
# Промежуточная выплата в турнире
# Победа в турнире
# Награда из подарка
# Награда из подарка (турнирный билет)
# Получен турнирный приз (сателлит)
# Регистрация в турнире (сателлит)
# Ре-ентри в турнире
# Деньги получены
# Деньги отправлены
# Бай-ин The Deal
# Награда The Deal (деньги)
# Адд-он в турнире
# Турнир отменен (прокрутка вперед)
# Компенсация рейка турнира
