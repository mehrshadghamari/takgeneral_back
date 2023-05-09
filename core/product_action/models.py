from django.db import models
from product.models import Product
from account.models import MyUser

    



class Comment(models.Model):
    comment_status=(
        ('initial','initial'),
        ('active','active')
        )
    status = models.CharField(choices=comment_status,default='initial',max_length=10)
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]



class Reply(models.Model):
    comment = models.ForeignKey("product_action.Comment", on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]



class Like(models.Model):
    comment = models.ForeignKey("product_action.Comment", on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} likes {self.comment.content[:50]}'
