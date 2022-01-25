from django.db import models

# Create your models here.
from django.db.models import Avg

from accounts.models import User


class Market(models.Model):
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.id}, {self.name}"

    reg_date = models.DateTimeField('등록날짜', auto_now_add=True)
    update_date = models.DateTimeField('갱신날짜', auto_now=True)
    name = models.CharField('마켓이름', max_length=100)
    site_url = models.URLField('마켓사이트URL', max_length=100)
    email = models.EmailField('마켓대표이메일', max_length=100)
    master = models.OneToOneField(User, on_delete=models.CASCADE)
    review_point = models.FloatField('리뷰평점', default=0)

    # # 방법 2, 여전히 무식한 방법
    # @property
    # def review_point(self):
    #     return self.product_set.aggregate(Avg('review_point'))['review_point__avg']

    # # 방법 1, 무식한 방법
    # @property
    # def review_point(self):
    #     products = self.product_set.all()
    #     return sum([product.review_point for product in products]) / len(products)
