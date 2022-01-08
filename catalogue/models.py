from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=250)
    price = models.CharField(max_length=22, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    title = models.CharField(max_length=250, null=True)
    value = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return self.product


class ProductLink(models.Model):
    url = models.CharField(max_length=250, unique=True)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class ProductImageLink(models.Model):
    url = models.CharField(max_length=250)
    flag = models.BooleanField(default=False)

    def __str__(self):
        return self.url
