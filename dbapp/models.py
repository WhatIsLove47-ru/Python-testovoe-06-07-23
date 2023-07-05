from django.db import models

# Create your models here.
class Query(models.Model):
    query_text = models.CharField(max_length=200)
