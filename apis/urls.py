from django.urls import path
from .views import *

urlpatterns = [
    # Menu
    path('menus/', MenuListCreateView.as_view(), name='menu_list'),
    path('menus/<int:pk>/', MenuRetrieveUpdateDestroyView.as_view(), name='menu'),

    # Kategori
    path('categories/', CategoryListCreateView.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='category'),

    # Stol
    path('tables/', TableListCreateView.as_view(), name='table_list'),
    path('tables/<int:pk>/', TableRetrieveUpdateDestroyView.as_view(), name='table'),

    # Bill
    path('bills/', BillListCreateView.as_view(), name='bill_list'),
    path('bills/<int:pk>/', BillRetrieveUpdateDestroyView.as_view(), name='bill'),

    # Order
    path('orders/', OrderListCreateView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyView.as_view(), name='order'),

    # Customer
    path('customers/', CustomerListCreateView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', CustomerRetrieveUpdateDestroyView.as_view(), name='customer'),

    # Payment
    path('payments/', PaymentListCreateView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyView.as_view(), name='payment'),
]
