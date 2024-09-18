from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

# Get the custom user model (or default user model if not customized)
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Using CharField for password to ensure proper validation and write-only field
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Confirmation field for password

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'bio', 'profile_picture']  # Ensure password2 is included
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    # Validate that password and password2 fields match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # Overriding create method to handle user creation
    def create(self, validated_data):
        # Remove password2 from validated data since it's not used for creation
        validated_data.pop('password2')

        # Create the user using Django's create_user method, which handles password hashing
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )

        # Create a token for the new user
        Token.objects.create(user=user)

        return user
