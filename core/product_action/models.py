from django.db import models
from product.models import Product
from account.models import MyUser
from django.core.validators import MaxValueValidator, MinValueValidator



class Comment(models.Model):
    comment_status = (
        ('initial', 'initial'),
        ('active', 'active')
    )
    status = models.CharField(choices=comment_status,
                              default='initial', max_length=10)
    product = models.ForeignKey(
        "product.Product", on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE)
    user_alias_name = models.CharField(max_length=64,default='alias')
    content = models.TextField()
    suggest_me=models.BooleanField(null=True,default=None)
    kefiyat_rate = models.FloatField(
        validators=[MaxValueValidator(5.0), MinValueValidator(1.0)],default=0
    )
    arzesh_rate = models.FloatField(
        validators=[MaxValueValidator(5.0), MinValueValidator(1.0)],default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def likes_count(self):
        return self.likes.filter(like_vote=True ,dislike_vote=False).count()

    @property
    def diss_likes_count(self):
        return self.likes.filter(dislike_vote=True,like_vote=False).count()

    def __str__(self):
        return self.content[:50]





class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    like_vote = models.BooleanField(default=False)
    dislike_vote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user}  {self.comment.content[:50]}'



class Reply(models.Model):
    comment = models.ForeignKey(
        "product_action.Comment", on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey("account.MyUser", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]