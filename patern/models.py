from django.db import models
from django.shortcuts import reverse


class PatternType(models.Model):
    pattern_name = models.CharField(max_length=50)

    def __str__(self):
        return self.pattern_name

    def del_absolute_url(self):
        return reverse('pattern:del-type', kwargs={"pk": self.pk})

    def create_body(self):
        return reverse('pattern:new-body', kwargs={"pk": self.pk})


class PatternBody(models.Model):
    pattern_type = models.ForeignKey(PatternType,
                                     on_delete=models.CASCADE,
                                     related_name='pattern_b',
                                     )
    pattern = models.CharField(max_length=100, verbose_name='Паттерн')

    def del_absolute_url(self):
        return reverse('pattern:del-body', kwargs={"pk": self.pk})

    def remake_action_url(self):
        return reverse('pattern:remake-action', kwargs={'pk': self.pk})

    def __str__(self):
        return self.pattern
