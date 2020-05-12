from django.db import models
from django.urls import reverse


class Player(models.Model):
    class Meta:
        ordering = ['pk']
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def del_absolute_url(self):
        return reverse('player:del-player', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('player:detail-player', kwargs={'pk': self.pk})

    def add_document(self):
        return reverse('files:upload-pk', kwargs={'pk': self.pk})
