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
