from rest_framework import viewsets, status # type: ignore
from rest_framework.response import Response    # type: ignore
from rest_framework.decorators import api_view  # type: ignore
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
import requests # type: ignore


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer

@api_view(['GET'])
def get_destinations_for_account(request, account_id):
    try:
        account = Account.objects.get(account_id=account_id)
    except Account.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    
    destinations = Destination.objects.filter(account=account)
    serializer = DestinationSerializer(destinations, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def receive_data(request):
    if request.method != 'POST':
        return Response({'error': 'Invalid method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    cl_x_token = request.headers.get('CL-X-TOKEN')
    if not cl_x_token:
        return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        account = Account.objects.get(app_secret_token=cl_x_token)
    except Account.DoesNotExist:
        return Response({'error': 'Un Authenticate'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        data = request.data
    except ValueError:
        return Response({'error': 'Invalid Data'}, status=status.HTTP_400_BAD_REQUEST)
    
    destinations = account.destinations.all()
    for destination in destinations:
        headers = destination.headers
        if destination.http_method.upper() == 'GET':
            response = requests.get(destination.url, headers=headers, params=data)
        elif destination.http_method.upper() in ['POST', 'PUT']:
            response = requests.request(destination.http_method, destination.url, headers=headers, json=data)
        else:
            continue
        print(f"Response from {destination.url}: {response.status_code} {response.text}")
    
    return Response({'status': 'success'}, status=status.HTTP_200_OK)
