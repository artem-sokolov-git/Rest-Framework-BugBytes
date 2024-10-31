import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum
from api.models import Product, Order, OrderItem


class Command(BaseCommand):
    help = "Creates application data"

    def handle(self, *args, **kwargs):
        # get or create superuser
        superuser = User.objects.filter(username="superuser").first()
        if not superuser:
            superuser = User.objects.create_superuser(
                username="superuser", password="superuser123"
            )

        # get or create customer
        customer = User.objects.filter(username="customer").first()
        if not customer:
            customer = User.objects.create_user(
                username="customer", password="customer123", email="customer@gmail.com"
            )

        # create products
        products = [
            Product(
                name="A Scanner Darkly",
                description=lorem_ipsum.paragraph(),
                price=Decimal("12.99"),
                stock=4,
            ),
            Product(
                name="Coffee Machine",
                description=lorem_ipsum.paragraph(),
                price=Decimal("70.99"),
                stock=6,
            ),
            Product(
                name="Velvet Underground & Nico",
                description=lorem_ipsum.paragraph(),
                price=Decimal("15.99"),
                stock=11,
            ),
            Product(
                name="Enter the Wu-Tang (36 Chambers)",
                description=lorem_ipsum.paragraph(),
                price=Decimal("17.99"),
                stock=2,
            ),
            Product(
                name="Digital Camera",
                description=lorem_ipsum.paragraph(),
                price=Decimal("350.99"),
                stock=4,
            ),
            Product(
                name="Watch",
                description=lorem_ipsum.paragraph(),
                price=Decimal("500.05"),
                stock=0,
            ),
        ]

        # The bulk_create method allows you to insert multiple model objects
        # into the database in a single query, which speeds up execution
        # for large amounts of data.
        Product.objects.bulk_create(products)
        products = Product.objects.all()

        # Create an order and assign it to a customer.
        for _ in range(3):
            # create an Order with 2 order items
            order = Order.objects.create(user=customer)
            for product in random.sample(list(products), 2):
                OrderItem.objects.create(
                    order=order, product=product, quantity=random.randint(1, 3)
                )
