from django.urls import path
from .views import (UserCreateView, UserLoginView, UserLogoutView,
                    setProduct, product_detail, product_delete, get_product_img)

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),

    path('product/create/', setProduct.as_view(), name='product-create'),
    path('product/update/', setProduct.as_view(), name='product-update'),
    path('product/get/<int:pk>/', product_detail, name='product-detail'),
    path('product/getimg/<int:pk>/', get_product_img, name='product-image'),
    path('product/delete/<int:pk>/', product_delete, name='product-delete'),
]
