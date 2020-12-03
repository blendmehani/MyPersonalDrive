from django.db import models
from accounts import models as account_model


# Create your models here.
# class Docs(models.Model):
#     docId = models.AutoField()
#     parentId = models.IntegerField(blank=True,null=True)
#     accountId = models.ForeignKey(account_model.Accounts, on_delete=models.CASCADE)
#     docType = models.CharField(choices='D''F''I')
#     docName = models.TextField(max_length=100)
