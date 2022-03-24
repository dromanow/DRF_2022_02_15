from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate
from .views import AuthorModelViewSet
from .models import Author, Bio
from django.contrib.auth.models import User
from mixer.backend.django import mixer


class TestAuthorApi(TestCase):

    def test_get_list(self):
        factory = APIRequestFactory()
        user = User.objects.create_superuser('denis', email='test@mail.com', password='qwerty')
        request = factory.get('/api/authors')
        force_authenticate(request, user)
        view = AuthorModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_list_1(self):
        factory = APIRequestFactory()
        request = factory.get('/api/authors')
        view = AuthorModelViewSet.as_view({'get': 'list'})
        Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_2(self):
        client = APIClient()
        response = client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_get_list_3(self):
        client = APIClient()
        Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        response = client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class TestAuthorClientApi(APITestCase):
    def setUp(self) -> None:
        self.author = mixer.blend(Author, birthday_year=1799)
        self.bio = mixer.blend(Bio, author__birthday_year=1800)
        self.admin = User.objects.create_superuser('denis', email='test@mail.com', password='qwerty')

    def test_get_list(self):
        self.client.login(username='denis', password='qwerty')
        self.client.logout()
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_1(self):
        self.client.force_login(self.admin)
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
