from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password

# Get the Custom User model
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Adding a write-only password field with validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Password confirmation

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'bio', 'profile_picture']

    # Validate that password and password2 are the same
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # Overriding the create method to handle user creation
    def create(self, validated_data):
        # Remove password2 as we don't need it for user creation
        validated_data.pop('password2')

        # Creating the user with the provided username and password
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None)
        )

        # Create a token for the newly created user
        Token.objects.create(user=user)

        return user
