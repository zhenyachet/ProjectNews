from django.db import models

class Account(models.Model):
    account = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return self.account


class Twit(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, null=False)
    text = models.TextField(null=False, default='Some text of twitter')
    release_date = models.DateField()
    hash_tags = models.TextField(null=True)

