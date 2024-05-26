from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account, Destination

class AccountTests(APITestCase):

    def setUp(self):
        self.account = Account.objects.create(email="test@example.com", name="Test Account")
        self.destination1 = Destination.objects.create(url="http://example.com/webhook1", http_method="POST", headers={"Content-Type": "application/json"}, account=self.account)
        self.destination2 = Destination.objects.create(url="http://example.com/webhook2", http_method="GET", headers={"Content-Type": "application/json"}, account=self.account)

    def test_delete_account(self):
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify the account is deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the destinations are deleted
        destination_url = reverse('destination-list')
        response = self.client.get(destination_url, {'account': self.account.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
