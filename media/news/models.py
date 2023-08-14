from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.TimeField(auto_now=True)

class Comment(models.Model):
    content = models.CharField(max_length=500)
    created_at = models.TimeField(auto_now=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)