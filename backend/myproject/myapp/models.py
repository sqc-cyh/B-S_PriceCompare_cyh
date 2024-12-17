from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator

class Users(AbstractUser):
    username = models.CharField(max_length=100, unique=True)  # 确保用户名唯一
    email = models.EmailField(unique=True)  # 确保邮箱唯一

    class Meta:
        app_label = 'myapp'

class Product(models.Model):
    name = models.CharField(max_length=255)  # 产品名称
    image_url = models.URLField(max_length=255, validators=[URLValidator()])  # 产品图片URL
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # 产品价格，允许为空
    platform = models.CharField(max_length=50, default='suning')  # 默认平台
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间
    updated_at = models.DateTimeField(auto_now=True)  # 更新时间
    search_time = models.DateTimeField(null=True, blank=True)  # 搜索时间，允许为空
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_at']  # 按创建时间降序排列
class PriceAlert(models.Model):
    username = models.CharField(max_length=100,default = 1)  # 存储用户名
    name = models.CharField(max_length=255)  # 商品名称
    image_url = models.URLField(max_length=255, validators=[URLValidator()], unique=True)  # 商品图片URL，设置为唯一
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 当前价格
    updated_at = models.DateTimeField(auto_now=True)  # 最后更新时间

    class Meta:
        verbose_name = 'Price Alert'
        verbose_name_plural = 'Price Alerts'
        ordering = ['-updated_at']  # 按更新时间降序排列
        
    def __str__(self):
        return f"{self.name} - ${self.price if self.price else 'N/A'}"