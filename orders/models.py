from django.db import models

PIZZA_TYPE = (
    ('veg', 'VEG'),
    ('non_veg', 'NON VEG')
)
PIZZA_SIZE = (
    ('regular', 'Regular'),
    ('medium', 'Medium'),
    ('large', 'Large')
)
ORDER_STATUS = (
    ('confirmed', 'Confirmed'),
    ('preparing', 'Preparing'),
    ('out_for_delivery', 'Out for Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled')
)


class GenericModel(models.Model):
    created_at = models.DateTimeField(verbose_name="Created at", auto_now_add=True)
    modified_at = models.DateTimeField(verbose_name="Modified at", auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Customer(GenericModel):
    customer_name = models.CharField(max_length=100)
    customer_address = models.TextField()
    customer_phone = models.CharField(max_length=15)

    def __str__(self):
        return 'Customer - ' + self.customer_name


class Pizza(GenericModel):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=PIZZA_TYPE, default='veg', max_length=10)
    size = models.CharField(choices=PIZZA_SIZE, default='regular', max_length=30)

    def __str__(self):
        return 'Pizza - ' + self.name

class Order(GenericModel):
    status = models.CharField(choices=ORDER_STATUS, default='confirmed', max_length=20)
    pizza_list = models.ManyToManyField(Pizza)
    ordered_by = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return 'Order #' + str(self.id)

    def get_pizza_list_base_action(self):
        return [{'id': pizza.id, 'action': 'do_nothing'} for pizza in self.pizza_list.all()]

