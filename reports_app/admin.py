from django.contrib import admin
from .models import SupportPost,ScamPost,Downvote

# Register your models here.
admin.site.register(ScamPost)
admin.site.register(SupportPost)
admin.site.register(Downvote)