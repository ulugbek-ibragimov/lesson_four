import random
from django.core.management.base import BaseCommand
from apps.product.models import *


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        users = self.create_users()
        categories = self.create_categories()
        products = self.create_products(categories)
        orders = self.create_order(users)
        self.create_order_items(orders, products)

    @staticmethod
    def create_users():
        users = []
        for i in range(1,31):
            user = User.objects.create_user(username=f"User {i}")
            users.append(user)
        return users

    @staticmethod
    def create_categories():
        categories = []
        for i in range(20):
            category = Category.objects.create(title=f"Category {i+1}")
            categories.append(category)
        return categories

    @staticmethod
    def create_products(categories: list):
        products = []
        for i in range(100):
            product = Product.objects.create(
                title=f'Product {i+1}',
                price=random.uniform(5000.00, 50000.00),
                description=f'Description {i+1}',
                stock=random.randint(1, 50),
                is_active=bool(random.randint(0, 2)),
                attributes={'color': random.choice(['red', 'blue', 'black']),
                            'weight': random.choice(['200', '500', '300', '600'])},
                category=random.choice(categories)
            )
            products.append(product)

        return products

    @staticmethod
    def create_order(users: list):
        orders = []
        for i in range(30):
            order = Order.objects.create(
                user=random.choice(users),
                status=random.choice(['pending', 'delivered', 'shipped'])
            )
            orders.append(order)
        return orders

    @staticmethod
    def create_order_items(orders: list, product: list):
        for i in range(len(orders)):
            for j in range(random.randint(1, 10)):
                OrderItem.objects.create(
                    order=orders[i],
                    product=random.choice(product),
                    quantity=random.randint(1, 4)
                )
