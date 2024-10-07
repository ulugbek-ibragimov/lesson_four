
#1)
from django.contrib.auth.models import User
from django.db.models import Count, Q, Sum
users_with_orders_count = User.objects.annotate(orders_count=Count('orders'))
# printing out number of orders of every users(we have 30 users)
for user in users_with_orders_count:
    print(user.oreders_count)

users_with_orders_prices_sum = User.objects.annotate(orders_price_sum=Sum('orders__items__product__price'))
# printing out sum of prices of all orders of user (for 30 users)
for user in users_with_orders_prices_sum:
    print('user.orders_price_sum')

users_with_unique_products_count = User.objects.annotate(unique_products_count=Count('orders__items', filter=Q(oreders__items__quantity=1)))
# printing out number of unique products of user (for 30 users)
for user in users_with_unique_products_count:
    print('user.unique_products_count')

#2)
from apps.product.models import Order, OrderItem
from django.db.models import Subquery, Prefetch, OuterRef
latest_order_subquery = Order.objects.filter(user=OuterRef('pk')).order_by('-created_at')
users_with_latest_order = User.objects.annotate(latest_order_id=Subquery(latest_order_subquery.values('id')[:1]))
orders_with_detail = Order.objects.prefetch_related(Prefetch('items', queryset=OrderItem.objects.select_related('product')))
for user in users_with_latest_order:
    if user.latest_order_id:
        latest_order=orders_with_detail.get(pk=latest_order_id)
        print(f"{latest_order.id}  {latest_order.status}  {latest_order.created_at})
    else:
        print("net zakazov")

#3)
from apps.product.models import Product
def FilterJSON(data):
    filtered_products = Product.objects.filter(attributes__contains=data)
    return filtered_products
for product in filtered_products:
    print(f"Product {product.title}, attributes {product.attributes}")

#4)
from apps.product.models import Order, OrderItem
from django.db.models import Prefetch
orders_with_detail = Order.object.prefetch_related(Prefetch('items', queryset=OrderItem.objects.select_related('product__category')))
for order in orders_with_detail:
    for item in order.items.all():
        print(f"product: {item.product.title} category: {item.product.category.title}")

#5)
from django.db.models import Sum, F, Count, FloatField
from django.contrib.auth.models import User

users_with_mean_price = User.objects.annotate(
    order_count=Count('orders'),
    total_price=Sum(
        F('orders__items__product__price') * F('orders__items__quantity'),
        output_field=FloatField()
    )
).annotate(
    mean_price=F('total_price') / F('order_count')
).filter(mean_price__gte=500)

for user in users_with_mean_price:
    print(f"User {user.username}. Number of orders - {user.order_count}. Sum of all prices of orders - {user.total_price}")

#6)
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import timedelta, datetime
from apps.product.models import Order

end_date = timezone.now()
start_date = end_date - timedelta(days=365)

orders = (
    Order.objects.filter(created_at__range=[start_date,end_date])
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(
       total_orders=Count('id'),
       total_price=Sum(F('items__quantity') * F('items__product__price'))
    )
    .order_by('month')
)

for order_summary in orders:
    print(f"Month: {order_summary['month']}, Total Orders: {order_summary['total_orders']}, Total Price: {order_summary['total_price']}")

#7)
from apps.product.models import Order, Product

low_stock_products=Product.objects.filter(stock__lt=5)
orders_to_update = Order.objects.filter(items__product__in=low_stock_products)
orders_to_update.update(status='on hold')

#8)
from apps.product.models import Product
from django.db.models import Sum

products = Product.objects.annotate(
    total_sold=Sum('items__quantity')
).filter(
    total_sold__gt=10,
    stock__lt=10
).values('title', 'total_sold', 'stock')


