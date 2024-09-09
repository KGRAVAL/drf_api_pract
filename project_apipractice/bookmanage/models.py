from django.db import models


class BookData(models.Model):
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    book_price = models.DecimalField(max_digits=7, decimal_places=2)
    published_date = models.DateField()
    copies_available = models.IntegerField()
    available_sw_cpy = models.BooleanField(default=False)
