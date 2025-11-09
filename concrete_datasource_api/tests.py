from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class UserTests(APITestCase):
    def test_register_user(self):
        url = reverse('register')
        data = {
            "email": "rakoto@example.com",
            "username": "rakoto",
            "password1": "abc123",
            "password2": "abc123"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['email'], data['email'])

    def test_register_user_password_mismatch(self):
        url = reverse('register')
        data = {
            "email": "rakoto2@example.com",
            "username": "rakoto2",
            "password1": "abc123",
            "password2": "wrongpass"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "rakoto@example.com",
            "username": "rakoto",
            "password": "abc123"
        }
        register_url = reverse('register')
        response = self.client.post(register_url, {
            "email": self.user_data["email"],
            "username": self.user_data["username"],
            "password1": self.user_data["password"],
            "password2": self.user_data["password"]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data['token']

    def test_login_valid_user(self):
        url = reverse('login')
        data = {"email": self.user_data["email"], "password": self.user_data["password"]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_user(self):
        url = reverse('login')
        data = {"email": "wrong@example.com", "password": "abc123"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)


class ApplicationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "rakoto@example.com",
            "username": "rakoto",
            "password": "abc123"
        }
        # Enregistrer l'utilisateur
        register_url = reverse('register')
        response = self.client.post(register_url, {
            "email": self.user_data["email"],
            "username": self.user_data["username"],
            "password1": self.user_data["password"],
            "password2": self.user_data["password"]
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.token = response.data['token']

        # Préparer le client avec token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_create_application(self):
        url = reverse('create_application')
        data = {"first_name": "Rochel", "last_name": "Soniarimamy"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], "Rochel")
        self.assertFalse(response.data['confirmed'])

    def test_confirm_application(self):
        # Créer l'application d'abord
        response = self.client.post(reverse('create_application'), {
            "first_name": "Rochel",
            "last_name": "Soniarimamy"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        app_id = response.data['id']

        # Confirmer l'application
        url = reverse('confirm_application', args=[app_id])
        data = {"confirmed": True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['confirmed'])

    def test_confirm_application_not_found(self):
        url = reverse('confirm_application', args=[999])
        data = {"confirmed": True}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
