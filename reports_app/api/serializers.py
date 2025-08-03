from rest_framework import serializers
from reports_app.models import ScamPost,SupportPost,Downvote

class SupportPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportPost
        #fields = "__all__"
        exclude = ['scampost','supporter']
        read_only_fields=["id","created_at"]
        def validate_evidence_link(self, value):
            if not value.startsWith(('http://', 'https://')):
                raise serializers.ValidationError("Evidence link must be a valid URL starting with http:// or https://")
            return value
        def validate_description(self,value):
            if not value.strip():
                raise serializers.ValidationError("Description cannot be empty")
            if len(value.strip()) < 50:
                raise serializers.ValidationError("Description must be at least 50 characters long")
            return value.strip()
        
        
class ScamPostSerializer(serializers.ModelSerializer):
     support_evidence = SupportPostSerializer(many=True, read_only=True)
     country_name = serializers.CharField(source='country.name', read_only=True)
     downvote_count = serializers.SerializerMethodField()
     is_downvoted = serializers.SerializerMethodField()
     class Meta:
         model = ScamPost
         fields =[
            'id', 'scammer_name', 'country_name', 
            'isglobal', 'created_at','support_evidence','downvote_count','is_downvoted'
        ]
         read_only_fields = ['id', 'created_at', 'support_evidence',]
     def get_downvote_count(self,obj):
         return obj.downvotes.count()
     def get_is_downvoted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Downvote.objects.filter(user=request.user, post=obj).exists()
        return False
class DownvoteSerializer(serializers.ModelSerializer):
      class Meta:
          model = Downvote
          fields =['id', 'post', 'created_at']
          read_only =['user', 'created_at']