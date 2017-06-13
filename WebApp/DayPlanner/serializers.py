from rest_framework import serializers

class UserRegistrationSerializer(serializers.Serializer):
    objectValue = serializers.CharField(
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    objectId = serializers.CharField(
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    userName = serializers.CharField(
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    firstName = serializers.CharField(
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    lastName = serializers.CharField(
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    passwordOne = serializers.CharField(
        style={'input_type': 'password'},
        required=False, 
        allow_blank=False, 
        max_length=100
    )
    passwordTwo = serializers.CharField(
        style={'input_type': 'password'},
        required=False, 
        allow_blank=False, 
        max_length=100
    )
