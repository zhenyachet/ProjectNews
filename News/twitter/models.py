from django.db import models



class Account(models.Model):
    account = models.CharField(max_length=100, unique=True, null=False)
    acc_id = models.CharField(max_length=15, unique=True, null=False, default='00000000')
    def __str__(self):
        return self.account


class Twit(models.Model):
    twitter_id = models.CharField(max_length=20, unique=True, primary_key=True)
    twitter_user = models.CharField(max_length=200)
    text = models.TextField(null=False, default='Some text of twitter')
    release_date = models.DateField()
    hash_tags = models.TextField(null=True)


