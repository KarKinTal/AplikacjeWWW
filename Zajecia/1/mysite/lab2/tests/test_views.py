from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Osoba

class OsobaListViewTest(TestCase):
    def setUp(self):
        self.user_with_permission = User.objects.create_user(username='admin', password='adminpass')
        self.user_with_permission.user_permissions.add(Permission.objects.get(codename='can_view_other_persons'))

        self.user_without_permission = User.objects.create_user(username='user', password='userpass')

        self.osoba1 = Osoba.objects.create(imie="Adam", nazwisko="Kowalski", wlasciciel=self.user_with_permission)
        self.osoba2 = Osoba.objects.create(imie="Ewa", nazwisko="Nowak", wlasciciel=self.user_without_permission)

        self.client = APIClient()

    def test_user_with_permission_sees_all_osoby(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('osoba_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_user_without_permission_sees_own_osoby(self):
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('osoba_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['imie'], "Ewa")

    def test_unauthenticated_user_is_denied(self):
        response = self.client.get(reverse('osoba_list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)