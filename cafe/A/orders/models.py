from django.db import models
from accounts.models import User


class MenuItem(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    discount = models.IntegerField()
    serving_time_period = models.TimeField()
    estimated_time = models.TimeField()


class Table(models.Model):
    table_number = models.PositiveIntegerField()
    cafe_space_position = models.PositiveIntegerField()
    use = models.BooleanField(default=False)


class Order(models.Model):
    tables = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='torders')
    number = models.IntegerField()
    status = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uorders')
    receipts = models.ForeignKey('Receipt', on_delete=models.CASCADE, related_name='rorders')
    menu_items = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='morders')


class Receipt(models.Model):
    total_price = models.IntegerField()
    final_price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ureceipts')
