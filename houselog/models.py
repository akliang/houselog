from datetime import date, timedelta
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Houselog(models.Model):
    title = models.CharField(max_length=200)
    last_done = models.DateField()
    frequency = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.TextField(blank=True, null=True)

    @property
    def next_run(self):
        return self.last_done + timedelta(days=self.frequency)
    
    @property
    def status(self):
        now = date.today()
        time_delta = self.next_run - now
        soon_threshold = timedelta(days=7)
        if time_delta < timedelta(0):
            return "late"
        if time_delta < soon_threshold:
            return "soon"
        return "ok"

