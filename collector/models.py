from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Article(models.Model):
    source = models.CharField(max_length=50)
    url = models.TextField()
    content = models.TextField()
    title = models.CharField(max_length=100)
    title2 = models.CharField(max_length=100)
    timestamp = models.IntegerField()
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.url

    def was_published_recently(self, day_range=5):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=day_range)
