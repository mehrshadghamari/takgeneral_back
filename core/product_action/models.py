from django.db import models

# Create your models here.


class favorites(models.Model):
    pass



class comments (models.Model):
    comment_status=(
            ('initial','initial'),
            ('active','active')
            )
    status = models.CharField(choices=comment_status,max_length=10)
    description=models.TextField()

    reply=models.ForeignKey('self')
    



