from django.db import models

# Create your models here.
class Advisor(models.Model):
       id = models.AutoField(primary_key = True, unique = True,
        serialize = False)
       name = models.CharField(max_length = 50, blank = False)
       profile_pic_url = models.URLField(max_length = 200, blank = False,
        unique = True)
       def __str__(self):
        return self.name +', '+self.profile_pic_url
