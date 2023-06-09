from django.db import models

# Create your models here.


class AmazonProduct(models.Model):
    product_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=50)
    rating = models.CharField(max_length=10)
    reviews = models.CharField(max_length=50)
    availability = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name