from django.db import models


class Document(models.Model):
    excel = models.FileField(upload_to='uploads')
