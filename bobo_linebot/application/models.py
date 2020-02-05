from django.db import models

class users(models.Model):
    uid = models.CharField(max_length=50, null = False)
    datatest = models.CharField(max_length=50, null = False)
<<<<<<< HEAD
=======
    #last_send_time = models.TimeField()
>>>>>>> d5b5899d5c38044c8073fb6bda6d1d0ff2b381e8
    def __str__(self):
        return self.uid