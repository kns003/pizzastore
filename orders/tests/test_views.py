from django.shortcuts import reverse

from rest_framework.test import APITestCase

from orders.models import Order, Customer, Pizza


class TestApi(APITestCase):
    def setUp(self):
        # create pizzas
        self.pizza_regular = Pizza(name='Margherita')
        self.pizza_regular.save()
        self.pizza_medium = Pizza(name='Cheese & Corn', size='medium', type='veg')
        self.pizza_medium.save()
        self.pizza_large = Pizza(name='Chicken delight', size='medium', type='non-veg')
        self.pizza_large.save()
        self.customer = Customer(customer_name='Madhuri', customer_address='Ecity Bangalore',
                                 customer_phone='9483917071')
        self.customer.save()
        self.delivered_order = Order.objects.create(ordered_by=self.customer, status='delivered')
        self.delivered_order.pizza_list.add(self.pizza_medium)
        self.delivered_order.save()


    def test_order_creation(self):
        response = self.client.post(reverse('orders-list'), {
            'ordered_by': {'customer_name': "Shashank",
                           "customer_address": "HSR Layout Bangalore",
                           "customer_phone": "9535441964"},
            "pizza_list": [{"id": self.pizza_regular.id}, {"id": self.pizza_medium.id}],
        }, format='json')

        # assert a created status code was returned
        self.assertEqual(201, response.status_code)


    def test_retrieve_order(self):
        response = self.client.post(reverse('orders-list'), {
            'ordered_by': {'customer_name': "Shashank",
                           "customer_address": "HSR Layout Bangalore",
                           "customer_phone": "9535441964"},
            "pizza_list": [{"id": self.pizza_medium.id}],
        }, format='json')

        response = self.client.get(reverse('orders-list'), format='json')
        self.assertEqual(len(response.data['results']), Order.objects.all().count())


    def test_updating_order_from_customer_end(self):
        order = Order.objects.create(
            ordered_by=self.customer,
        )
        order.pizza_list.add(self.pizza_regular)
        order.save()
        response = self.client.put(reverse('orders-detail', kwargs={'pk': order.id}), {
            'ordered_by': {'id': self.customer.id},
            'status': "confirmed",
            "pizza_list": [{"id": self.pizza_regular.id, "action": "remove"},
                           {"id": self.pizza_large.id, "action": "add"}],
        }, format="json")
        # check info returned has the update
        self.assertEqual(self.pizza_large.id, response.data['pizza_list'][0]['id'])

    def test_updating_order_from_restuarant_end(self):
        order = Order.objects.create(
            ordered_by=self.customer,
        )
        order.pizza_list.add(self.pizza_regular, self.pizza_medium)
        order.save()
        url = reverse('orders-detail', kwargs={'pk': order.id})
        data = {"status": "out_for_delivery",
                "ordered_by": {'id': self.customer.id},
                "pizza_list": order.get_pizza_list_base_action()}
        response = self.client.put(url, data,format="json")
        order.refresh_from_db()
        self.assertEqual(response.data['status'], order.status)

    def test_status_change_when_order_out_for_delivery(self):
        '''
        Adding pizza when order is out for delivery
        :return:
        '''
        order = Order.objects.create(
            ordered_by=self.customer,
        )
        order.pizza_list.add(self.pizza_medium)
        order.status = 'out_for_delivery'
        order.save()
        response = self.client.put(reverse('orders-detail', kwargs={'pk': order.id}), {
            "pizza_list": [{"id": self.pizza_regular.id, "action": "add"},
                           {"id": self.pizza_large.id, "action": "add"}],
            "status": 'out_for_delivery',
            'ordered_by': {'id': self.customer.id}
        }, format="json")
        self.assertEqual(400, response.status_code)

    def test_change_order_status_when_delivered(self):
        response = self.client.put(reverse('orders-detail', kwargs={'pk': self.delivered_order.id}), {
            'status': 'confirmed',
            "ordered_by": {'id': self.customer.id},
            "pizza_list": self.delivered_order.get_pizza_list_base_action()
        }, format="json")
        self.assertEqual(400, response.status_code)

    def test_remove_order(self):
        order = Order.objects.all().last()
        self.client.delete(reverse('orders-detail', kwargs={'pk': self.delivered_order.id}), format='json')
        # check status
        order.refresh_from_db()
        self.assertEqual('cancelled', order.status)
