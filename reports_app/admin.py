from django.contrib import admin
from .models import SupportPost,ScamPost

# Register your models here.
admin.site.register(ScamPost)
admin.site.register(SupportPost)