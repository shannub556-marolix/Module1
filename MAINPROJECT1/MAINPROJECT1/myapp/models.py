from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField(null=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.name

class CartItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField(default=0)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.quantity} x {self.product.name}'

class address(models.Model):
	name=models.CharField(max_length=50)
	phone_number=models.IntegerField()
	pincode=models.IntegerField()
	state=models.CharField(max_length=50)
	city=models.CharField(max_length=50)
	colony=models.CharField(max_length=50)
	street=models.CharField(max_length=50)



