import os
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_token(request):
    user = request.data.get('username')
    password = request.data.get('password')

    print(f"username: {user}, password: {password}")

    url = f"{os.environ.get('PROTOCOL')}://{os.environ.get('IP_SERVER')}:{os.environ.get('PORT')}/fireedge/api/auth"
    print (url)
    payload = {
        'user': user,
        'token': password
    }
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        data = response.json()
        return Response({'token': data['data']['token']}, status=status.HTTP_200_OK)
    else:
        print(response.text)  # Print error message for debugging
        return Response({'error': 'Failed to retrieve token'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
