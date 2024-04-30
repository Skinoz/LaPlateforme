from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.conf import settings
import requests

class Token(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = User.objects.filter(username=username).first()
        
        if user and user.check_password(password):
            url = f"{settings.PROTOCOL}://{settings.IP_SERVER}:{settings.PORT}/fireedge/api/auth"
            payload = {
                'user': settings.OPENNEBULA_USER,
                'password': settings.OPENNEBULA_PASSWORD
            }
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return Response({'token': data['data']['token']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to retrieve token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
