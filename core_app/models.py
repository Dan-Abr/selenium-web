from django.db import models


class E2ETestParams(models.Model):
    link = models.TextField()  # link --> url

    # ... list_of actions = [] ?

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


# Create your models here.
class E2ETestResults(models.Model):
    link = models.TextField()  # link --> url
    page_title = models.CharField(max_length=200)
    status = models.CharField(max_length=10)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.link[:20]  # link --> url