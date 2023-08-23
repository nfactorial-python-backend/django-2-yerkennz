from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=250)
    created_at = models.TimeField(auto_now=True)

    def has_comments(self):
        return Comment.objects.filter(news=self).exists()

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    content = models.CharField(max_length=500)
    created_at = models.TimeField(auto_now=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE)