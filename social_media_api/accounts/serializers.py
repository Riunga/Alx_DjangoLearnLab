from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
