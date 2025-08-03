from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
     confirmpassword = serializers.CharField(
        write_only= True,
        style = {'input_type': 'password'}
     )
     class Meta:
         model = User
         fields = ['email','username','password','confirmpassword']
         extra_kwargs = {
            'password':{'write_only':True}
         }
     def validate(self, attrs):
             if attrs['password'] != attrs['confirmpassword']:
                 raise serializers.ValidationError("Password did not match")
             if User.objects.filter(email__iexact=attrs['email']).exists():
                 raise serializers.ValidationError("The email is already in use!")
             return attrs
     def create(self, validated_data):
             validated_data.pop("confirmpassword")
             raw_password = validated_data.pop("password")
             user = User(**validated_data)
             user.set_password(raw_password)
             user.save()
             return user
             