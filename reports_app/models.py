from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User


class ScamPost(models.Model):
    
    scammer_name = models.CharField(max_length=100)
    socials = models.JSONField(default=list,blank=True,null=True)
    incidence_description = models.TextField()
    country = CountryField(blank=True,null=True)
    isglobal = models.BooleanField(default=False)
    evidence_drive_link =models.URLField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.scammer_name
    

class SupportPost(models.Model):
    supporter = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    description = models.TextField()
    evidence_link = models.URLField()
    created_at = models.DateField(auto_now_add=True)
    scampost = models.ForeignKey(ScamPost,on_delete=models.CASCADE,related_name='support_evidence',null=True,blank=True)
    def __str__(self):
        return self.description
    
class Downvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(ScamPost,on_delete=models.CASCADE,related_name='downvotes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post') 
    def __str__(self):
        return f"{self.user.username} downvoted {self.post.scammer_name}"