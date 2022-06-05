from django.db import models

# Create your models here.
class CrawlerTask(models.Model):
    link = models.TextField()
    title = models.CharField(max_length=200)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.link[:20]