from django.db import models
from category.models import Category
from django.utils.text import slugify
# Create your models here.
class Products(models.Model):
    product_name    = models.CharField(max_length=200,unique=True)
    slug            = models.SlugField(unique=True)
    description     = models.TextField(blank=True)
    price           = models.PositiveBigIntegerField()
    image           = models.ImageField(upload_to='photos/products')
    stock           = models.PositiveIntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'products'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.product_name

    def save(self):
        self.slug = slugify(self.product_name)
        super(Products,self).save()

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)


variation_category_choice=(
    ('color','color'),
    ('size','size'),
)
class Variation(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100,choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active   = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()
    def __str__ (self):
        return self.variation_value