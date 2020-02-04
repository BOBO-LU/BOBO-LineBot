from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50, null = False)
    datatest = models.CharField(max_length=50, null = False)
    #last_send_time = models.TimeField()
    def __str__(self):
        return self.uid