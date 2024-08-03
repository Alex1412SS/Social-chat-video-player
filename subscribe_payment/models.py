from django.db import models

class lvl_subscribe(models.Model):
    name = models.CharField(max_length=100)
    lvl = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    promocode = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + str(self.lvl)
