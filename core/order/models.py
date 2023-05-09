from django.db import models
from account.models import MyUser
from product.models import Product



class Order(models.Model):
	user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE, related_name='orders')
	paid = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('paid', '-updated')


	def __str__(self):
		return f'{self.user} - {str(self.id)}'


	# def get_total_price(self):
	# 	total = sum(item.get_cost() for item in self.items.all())
	# 	if self.discount:
	# 		discount_price = (self.discount / 100) * total
	# 		return int(total - discount_price)
	# 	return total


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
	price = models.IntegerField()
	quantity = models.IntegerField(default=1)

	
	



