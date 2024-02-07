from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    category=models.CharField(max_length=100,default='')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product_name
    
class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.PositiveIntegerField()
    date=models.DateField()
    
    def __str__(self):
        return self.user
