from django.db import models
from products.models import Product
from django.contrib.auth.models import User

# Create your models here.
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name='cart_items')
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name='cart_items')

    quantity = models.PositiveIntegerField()

    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user', 'product']]
    def __str__(self):
        return f"product: {self.product.title.capitaliZe()} in {self.user.username.cptitalize()} 's cart - Quantity : {self.quantity}"