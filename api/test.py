from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Product
from rest_framework.authtoken.models import Token


class testCreateUser(APITestCase):
    def test_user_created(self):
        url = reverse('user-create')
        data = {'username': 'test', 'email': 'test@example.com', 'password': '<PASSWORD>'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'test')

    def test_invalid_user(self):
        url = reverse('user-create')
        data = {'username': 'test', 'email': 'admin.com', 'password': '<PASSWORD>'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class loginTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login(self):
        url = reverse('user-login')
        data = {'username': 'testuser', 'password': '12345'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)

    def test_login_invalid_credentials(self):
        url = reverse('user-login')

        data = {'username': 'testuser', 'password': 'wrongpassword'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 401)


class logoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='<PASSWORD>')

        self.token = Token.objects.create(user=self.user)

    def test_logout(self):
        url = reverse('user-logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Token.objects.filter(key=self.token).exists())

    def test_logout_without_token(self):
        url = reverse('user-logout')

        response = self.client.post(url)

        self.assertEqual(response.status_code, 401)


class testCreateProduct(APITestCase):
    def test_product_created(self):
        url = reverse('product-create')
        data = {'name': 'test', 'description': 'test', 'price': '10.3', 'stock': '10'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, 'test')

    def test_invalid_product(self):
        url = reverse('product-create')
        data = {'name': 'test', 'description': 'test', 'price': '1111.3444', 'stock': '10'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class testUpdateProduct(APITestCase):
    def setUp(self):
        self.Product = Product.objects.create(id=6, name='test', description='test', price='10.2', stock='10')

    def test_product_updated(self):
        url = reverse('product-create')
        data = {'id': '6', 'name': 'product_test', 'description': 'test', 'price': '11.5', 'stock': '9'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().price, 11.5)

    def test_invalid_product(self):
        url = reverse('product-create')
        data = {'id': '6', 'name': 'product_test', 'description': 'test', 'price': '1111.3444', 'stock': '10'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class testDeleteProduct(APITestCase):
    def setUp(self):
        self.Product = Product.objects.create(id=6, name='test', description='test', price='10.2', stock='10')

    def test_product_deleted(self):
        url = reverse('product-delete', args=[6])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_product(self):
        url = reverse('product-delete', args=[8])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class testGetProduct(APITestCase):
    def setUp(self):
        self.Product = Product.objects.create(id=6, name='test', description='test', price='10.2', stock='10')

    def test_product_selected(self):
        url = reverse('product-detail', args=[6])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.count(), 1)

    def test_invalid_product(self):
        url = reverse('product-detail', args=[8])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class testGetProductsImg(APITestCase):
    def setUp(self):
        self.Product = Product.objects.create(id=6, name='test', description='test', price='10.2', stock='10', imagen='productos/puppy.png')
        self.Product = Product.objects.create(id=5, name='test', description='test', price='10.2', stock='10')
    def test_product_selected(self):
        url = reverse('product-image', args=[6])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    def test_invalid_product(self):
        url = reverse('product-image', args=[7])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_no_image_product(self):
        url = reverse('product-image', args=[5])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
