from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['category_name'] = instance.category.name  
        return data


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['menu_item_name'] = instance.menu_item.name  
        data['bill_id'] = instance.bill.id  
        data['total_price'] = instance.quantity * instance.menu_item.price  
        return data
    
class BillSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)
    # orders = serializers.StringRelatedField(many=True)
    # orders = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # orders = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='order_list')

    class Meta:
        model = Bill
        fields = ['table', 'customer', 'total_sum',"is_paid", 'orders']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['customer_name'] = instance.customer.name  
        data['customer_phone'] = instance.customer.phone 
        data['table_name'] = instance.table.table_name 
        return data




class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['customer_name'] = instance.customer.name  
        data['bill_id'] = instance.bill.id 
        return data