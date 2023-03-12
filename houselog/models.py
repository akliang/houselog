import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Houselog(models.Model):
    title = models.CharField(max_length=200)
    last_done = models.DateField()
    frequency = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def next_run(self):
        return self.last_done + datetime.timedelta(days=self.frequency)
