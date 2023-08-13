from django.db import models


class Order(models.Model):
    user = models.ForeignKey(
        "account.MyUser", on_delete=models.CASCADE, related_name='orders')
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('paid', '-updated')

    @property
    def total_price(self):
        return sum(item.sum_price for item in self.items.all())

    @property
    def total_final_price(self):
        return sum(item.sum_final_price for item in self.items.all())

    @property
    def total_discount_price(self):
        return sum(item.sum_discount_price for item in self.items.all())

    @property
    def total_count(self):
        return sum(item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='items')
    # product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    product = models.ForeignKey("product.ProductVariant", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def sum_final_price(self):
        return (self.product.price * (1 - (self.product.discount / 100))) * self.quantity

    @property
    def sum_price(self):
        return self.product.price * self.quantity

    @property
    def sum_discount_price(self):
        return self.sum_price - self.sum_final_price
