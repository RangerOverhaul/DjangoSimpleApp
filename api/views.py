from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse

from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, ProductSerializer
from .models import Product

import re


# Create your views here.

def validate_email(email):
    patron = r'^[\w\.-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9\.]+$'
    return re.match(patron, email)

class UserCreateView(APIView):
    """
    Create a new user.

    Args:
        POST request.username
        POST request.password
        POST request.email

    Returns:
        username, Http201: created

        exception Http500: Internal Server Error.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        same_username = request.data.get('username')
        same_email = request.data.get('email')
        password = request.data.get('password')
        if not validate_email(same_email):
            return Response({'message': 'Email address format'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=same_username).exists() or User.objects.filter(email=same_email).exists():
            return Response({'message': 'Username or email already taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User(username=same_username, email=same_email)
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'username': user.username, 'Description': 'User created'},
                        status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    Login a user created.

    Args:
        POST request.username.
        POST request.password.

    Returns:
        Token and user info.

        exception Http401: Unauthorized.
    """

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    """
    Logout a login user.

    Return:

        Http 201: Successfully logged out.
        exception Http401: Unauthorized.
    """

    def post(self, request, *args, **kwargs):
        token_key = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[-1]

        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            logout(request)
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


class setProduct(APIView):
    """
    Create a new product or update an existing product.
    """

    def post(self, request, *args, **kwargs):
        """
        Create a new product.
        :param request:
            :param name: Product name.
            :param price: Product price.
            :param description: Product description.
            :param stock: Product stock.
        :return:
            Http 201: Successfully saved product.
            :exception Http500: Internal Server Error.
        """
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_name = request.data['name']
        serializer.save()
        current_id = serializer.instance.id
        return Response({'message': f'Product {current_name} saved successfully',
                         'id': str(current_id)}, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        """
        Update an existing product.
        :param request:
            :param name: Product name.
            :param price: Product price.
            :param description: Product description.
            :param stock: Product stock.
        :return:
            Http 201: Successfully saved product.
            :exception Http404: Bad request.
        """
        try:
            if 'id' in request.data:
                product = Product.objects.get(pk=request.data['id'])
            else:
                return Response({'error': 'Hide id field to update'}, status=status.HTTP_400_BAD_REQUEST)
            current_name = product.name
            if 'name' in request.data:
                product.name = request.data['name']
                current_name = request.data['name']
            if 'price' in request.data:
                product.price = float(request.data['price'])
            if 'description' in request.data:
                product.description = request.data['description']
            if 'stock' in request.data:
                product.stock = int(request.data['stock'])
            if 'imagen' in request.data:
                product.imagen = request.data['imagen']
            product.save()
            return JsonResponse({'message': f'Product {current_name} updated successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=404)


@api_view(["GET"])
def product_detail(request, pk):
    """
    Retrieve details of an existing product.
    :param request:
        :param pk: Product ID.
    :return:
        Http 200: Successfully retrieved product.
        :exception Http404: Bad request.
    """
    try:
        current_product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return JsonResponse({'mensaje': f'Product with id {pk} does not exist'}, status=404)
    serializer = ProductSerializer(current_product)
    return Response(serializer.data)


@api_view(["DELETE", "GET"])
def product_delete(request, pk):
    """
    Delete an existing product.
    :param request:
        :param pk: Product ID.
    :return:
        Http 200: Successfully deleted product.
        :exception Http404: Bad request.
    """
    try:
        current_product = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        return JsonResponse({'mensaje': f'Product with id {pk} does not exist'}, status=404)
    current_name = current_product.name
    current_product.delete()
    return JsonResponse({'message': f'Product {current_name} deleted successfully'}, status=204)


@api_view(["GET"])
def get_product_img(request, pk):
    """
    Get an image of an existing product.
    :param request:
        :param pk: Product ID.
    :return:
        Http 200: Successfully retrieved product image plus the image in format jpeg.
        :exception Http404: Bad request.
    """
    try:
        product = Product.objects.get(pk=pk)
        if product.imagen:
            with open(product.imagen.path, "rb") as image_file:
                return HttpResponse(image_file.read(), content_type="image/jpeg")
        else:
            return HttpResponse("Image is not available for this product.", status=404)
    except Product.DoesNotExist:
        return HttpResponse("The product does not exist.", status=400)
