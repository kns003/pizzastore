from rest_framework import serializers
from .models import Order, Customer, Pizza, ORDER_STATUS

class CustomerUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Customer
        fields = ('id',)

class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ('created_at', 'modified_at', 'is_active')

class PizzaCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Pizza
        fields = ('id',)

class PizzaListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Pizza
        exclude = ('created_at', 'modified_at', 'is_active')

class PizzaUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    action = serializers.CharField(required=False)

    class Meta:
        model = Pizza
        fields = ('id', 'action')

class OrderListSerializer(serializers.ModelSerializer):
    ordered_by = CustomerCreateSerializer(many=False)
    pizza_list = PizzaCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('ordered_by', 'status', 'pizza_list')


class OrderCreateSerializer(serializers.ModelSerializer):
    ordered_by = CustomerCreateSerializer(many=False)
    pizza_list = PizzaCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('ordered_by', 'status', 'pizza_list')

    def create(self, validated_data):
        customer_info = validated_data.get('ordered_by', {})
        cust_instance, created = Customer.objects.get_or_create(
            customer_phone=customer_info.get('customer_phone'),
        )
        if created:
            cust_instance.customer_address = customer_info.get('customer_address')
            cust_instance.customer_name = customer_info.get('customer_name')
            cust_instance.save()
        else:
            # update the address if its changed for the next order
            cust_instance.customer_address = customer_info.get('customer_address', cust_instance.customer_address)
        pizza_list = validated_data.get('pizza_list', [])
        try:
            pizza_objects = [Pizza.objects.get(id=pizza_dict.get('id')) for pizza_dict in pizza_list]
        except Exception as e:
            raise serializers.ValidationError('Pizza Does not exist')
        order = Order.objects.create(ordered_by=cust_instance)
        for pizza in pizza_objects:
            order.pizza_list.add(pizza)
        order.save()
        return order

class OrderUpdateSerializer(serializers.ModelSerializer):
    ordered_by = CustomerUpdateSerializer(many=False)
    pizza_list = PizzaUpdateSerializer(many=True)

    class Meta:
        model = Order
        fields = ('ordered_by', 'status', 'pizza_list')


    def update(self, instance, validated_data):
        if instance.status == dict(map(reversed, ORDER_STATUS))['Delivered']:
            raise serializers.ValidationError("Status cannot be changed for a delivered Pizza")
        if instance.status == dict(map(reversed, ORDER_STATUS))['Cancelled']:
            raise serializers.ValidationError("Your order has been cancelled. You cannot change the status")

        customer_info = validated_data.get('ordered_by', {})
        if customer_info.get('id'):
            try:
                customer = Customer.objects.get(id=customer_info.get('id'))
            except Exception as e:
                raise serializers.ValidationError('Customer does not exist')
            customer.customer_address = customer_info.get('customer_address', instance.ordered_by.customer_address)
            customer.save()
        pizza_list =validated_data.get('pizza_list')

        if instance.status == dict(map(reversed, ORDER_STATUS))['Out for Delivery'] and len(pizza_list) > 0:
            raise serializers.ValidationError("You cannot edit your order now as the order is out for delivery")

        for pizza_dict in pizza_list:
            try:
                pizza = Pizza.objects.get(id=pizza_dict.get('id'))
            except Exception as e:
                raise serializers.ValidationError('Pizza Does not exist')
            if pizza_dict.get('action') == 'add':
                instance.pizza_list.add(pizza)
            elif pizza_dict.get('action') == 'remove':
                instance.pizza_list.remove(pizza)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance





