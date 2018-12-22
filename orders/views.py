from rest_framework import viewsets
from .models import Order,Customer, Pizza, ORDER_STATUS
from .serializers import CustomerCreateSerializer, PizzaListSerializer, OrderCreateSerializer, \
    OrderUpdateSerializer, OrderListSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderListSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        customer_name = self.request.query_params.get('customer_name', None)
        size = self.request.query_params.get('size', None)
        status = self.request.query_params.get('status', None)
        if customer_name is not None:
            queryset = queryset.filter(ordered_by__customer_name__icontains=customer_name)
        if size is not None:
            queryset = queryset.filter(pizza__size=size)
        if status is not None:
            queryset = queryset.filter(status=status)
        return queryset

    def create(self, request, *args, **kwargs):
        self.serializer_class = OrderCreateSerializer
        return viewsets.ModelViewSet.create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.serializer_class = OrderUpdateSerializer
        return viewsets.ModelViewSet.update(self, request, *args, **kwargs)


    def perform_destroy(self, instance):
        '''
        When an Order is DELETED/Removed, we set the status to cancelled in the backend.
        We don't want to do a hard delete by .delete()
        :param instance:
        :return:
        '''
        instance.status = dict(map(reversed, ORDER_STATUS))['Cancelled']
        instance.is_active = False
        instance.save()

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerCreateSerializer

class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaListSerializer
