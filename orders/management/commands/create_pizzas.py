from django.core.management import BaseCommand
from ...models import Pizza, PIZZA_SIZE, PIZZA_TYPE

class Command(BaseCommand):
    def handle(self, *args, **options):
        Pizza.objects.create(
            name='Veggie Delight',
            size=PIZZA_SIZE[0][0],
            type=PIZZA_TYPE[0][0]
        )

        Pizza.objects.create(
            name='Chicken Peproni',
            size=PIZZA_SIZE[1][0],
            type=PIZZA_TYPE[1][0]
        )

        Pizza.objects.create(
            name='Cheese & Corn',
            size=PIZZA_SIZE[2][0],
            type=PIZZA_TYPE[0][0]
        )

        print("Created 3 Pizzas")
