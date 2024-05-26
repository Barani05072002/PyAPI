from django.urls import path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from .views import AccountViewSet, DestinationViewSet, get_destinations_for_account, receive_data

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('accounts/<uuid:account_id>/destinations/', get_destinations_for_account, name='account-destinations'),
    path('server/incoming_data', receive_data, name='receive_data'),
]
