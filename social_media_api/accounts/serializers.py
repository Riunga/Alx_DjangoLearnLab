from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password

# Get the custom user model (or default user model if none exists)
User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly define password as a CharField to ensure it is properly validated and write-only
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)  # Password confirmation field

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'bio', 'profile_picture']  # Include password2
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    # Ensure both password and password2 fields match
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    # Overriding the create method to handle user creation
    def create(self, validated_data):
        # Remove password2 as it is not needed for actual user creation
        validated_data.pop('password2')

        # Create user using the default `create_user` method for password hashing
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture')
        )

        # Create a token for the user
        Token.objects.create(user=user)

        return user
