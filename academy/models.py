from django.db import models
from django.contrib.auth.models import User


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Request(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[('В ожидании', 'В ожидании'), ('Принял', 'Принял'), ('Отклонил', 'Отклонил')], default='В ожидании')

    def __str__(self):
        return f'{self.client.name} - {self.master.name}'
