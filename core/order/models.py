from django.db import models


class Order(models.Model):

    STATUS_CHOICES = (
        ("REQUEST", "REQUEST"),
        ("PENDING", "PENDING"),
        ("PROCESSING", "PROCESSING"),
        ("COMPLETED", "COMPLETED"),
    )

    user = models.ForeignKey(
        "account.MyUser",
        on_delete=models.CASCADE,
        related_name="orders",
    )
    address = models.OneToOneField(
        "account.Address",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="REQUEST",
    )
    authority = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        unique=True,
    )
    Payment_ref_id = models.IntegerField(
        null=True,
        blank=True,
        unique=True,
    )
    paid = models.BooleanField(
        default=False,
    )
    Payment_time = models.DateTimeField(
        null=True,
        blank=True,
    )
    receiver_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
    )
    receiver_phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = (
            "paid",
            "-updated",
        )

    @property
    def total_price(self):
        return int(sum(item.sum_price for item in self.items.all()))

    @property
    def total_final_price(self):
        return int(sum(item.sum_final_price for item in self.items.all()))

    @property
    def total_discount_price(self):
        return int(sum(item.sum_discount_price for item in self.items.all()))

    @property
    def total_count(self):
        return int(sum(item.quantity for item in self.items.all()))


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        "product.ProductVariant",
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField(
        default=1,
    )

    @property
    def sum_final_price(self):
        return (self.product.price * (1 - (self.product.discount / 100))) * self.quantity

    @property
    def sum_price(self):
        return self.product.price * self.quantity

    @property
    def sum_discount_price(self):
        return self.sum_price - self.sum_final_price
