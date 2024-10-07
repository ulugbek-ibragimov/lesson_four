from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Category name'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    title = models.CharField(_('Product name'), max_length=200)
    price = models.DecimalField(verbose_name=_('Product price'), max_digits=10, decimal_places=2)
    description = models.TextField(verbose_name=_('Product description'))
    stock = models.IntegerField(default=0, verbose_name=_('Product stock'))
    is_active = models.BooleanField(default=True, verbose_name=_('Active product'))
    attributes = models.JSONField(verbose_name=_('Product attributes'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date time created'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date time update'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Person'), related_name='orders')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date time created'), editable=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.get_status_display()}"

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name=_('Order'))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name=_('Product'))
    quantity = models.IntegerField(default=0, verbose_name=_('Quantity'))

    def __str__(self):
        return f"user {self.order.user.username}'s order for product {self.product.title}"

    class Meta:
        verbose_name = 'Orderitem'
        verbose_name_plural = 'Orderitems'

