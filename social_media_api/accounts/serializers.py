from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Define the password field with CharField and validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # Define password2 for confirmation
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'bio', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        # Ensure passwords match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        # Remove password2 since it's not needed for user creation
        validated_data.pop('password2')

        # Create user using the create_user method
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )

        # Create a token for the user
        Token.objects.create(user=user)

        return user
