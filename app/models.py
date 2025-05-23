from django.db import models
from decimal import Decimal
# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(max_length=150,unique=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'categories'
        verbose_name = 'category'
        db_table = 'category'

# category.products.all()

class Product(BaseModel):
    name = models.CharField(max_length=150)
    description = models.TextField(null=True,blank=True)
    price = models.DecimalField(max_digits=14,decimal_places=2)
    discount = models.PositiveIntegerField(default = 0)
    image = models.ImageField(upload_to='products/',null=True,blank=True)
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank = True
                                 )
    quantity = models.PositiveIntegerField(default=1)
    
    
    @property
    def discounted_price(self):
        if self.discount:
            return self.price * Decimal(f'{1 - self.discount / 100}')
        return self.price
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'products'
        verbose_name = 'product'
        db_table = 'product'
# product.discounted_price

# product.category

# 5 + '2'

# 0.1 + 0.1 + 0.1 = 0.3000000000004


class Order(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='orders',
                                null=True,
                                blank=True
                                )
    
    class Meta:
        db_table = 'order'
        

class Comment(BaseModel):
    class RatingChoices(models.IntegerChoices):
        ONE = 1
        TWO = 2
        THREE = 3
        FOUR = 4
        FIVE = 5
    name = models.CharField(max_length=100)
    email = models.EmailField() # @ 
    content = models.TextField()
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                related_name= 'comments',
                                null=True,
                                blank=True
                                )
    rating = models.IntegerField(choices=RatingChoices.choices,default=RatingChoices.THREE.value)
    
    def __str__(self):
        return f'{self.name} - {self.product}'
    
    


    

    