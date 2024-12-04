from django.contrib.auth.models import User, Permission
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from ..models import Osoba


class OsobaListViewTest(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.admin_user = User.objects.create_user(username="admin", password="adminpassword")

        permission = Permission.objects.get(codename="can_view_other_persons")
        self.admin_user.user_permissions.add(permission)

        Osoba.objects.create(imie="Jan", nazwisko="Kowalski", wlasciciel=self.user1)
        Osoba.objects.create(imie="Anna", nazwisko="Nowak", wlasciciel=self.user2)

    def test_unauthenticated_user_is_denied(self):
        """Nieautoryzowany użytkownik powinien otrzymać 401 Unauthorized."""
        url = reverse('osoba_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_without_permission_sees_own_osoby(self):
        """Użytkownik bez specjalnych uprawnień widzi tylko swoje osoby."""
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse('osoba_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['imie'], "Jan")

    def test_user_with_permission_sees_all_osoby(self):
        """Użytkownik z uprawnieniem `can_view_other_persons` widzi wszystkie osoby."""
        self.client.login(username="admin", password="adminpassword")
        response = self.client.get(reverse('osoba_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        imiona = [osoba['imie'] for osoba in response.data]
        self.assertIn("Jan", imiona)
        self.assertIn("Anna", imiona)