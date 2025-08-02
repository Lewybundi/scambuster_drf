from rest_framework import serializers
from reports_app.models import ScamPost,SupportPost

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
     class Meta:
         model = ScamPost
         fields =[
            'id', 'scammer_name', 'country_name', 
            'isglobal', 'created_at','support_evidence'
        ]
         read_only_fields = ['id', 'created_at', 'support_evidence',]