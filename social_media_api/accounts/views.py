from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterSerializer
from django.contrib.auth import authenticate

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Get the user's token after registration
            token = Token.objects.get(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
