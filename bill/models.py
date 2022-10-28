from django.db import models
import uuid

from django.shortcuts import redirect
from .models import *

# Create your models here.


class DateTimeMixin(models.Model):
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True




class ProductDescription(DateTimeMixin):
    name = models.CharField(max_length = 500, blank = True, null = True)
    price = models.IntegerField( blank = True, null = True)
    quantity = models.IntegerField( blank = True, null = True)

    def __str__(self):
        return self.name




def bill_number():

    bill_obj = Bill.objects.all().count()

    if bill_obj > 1:
        return int(bill_obj) + 1
    else:    
        return 1

class Bill(DateTimeMixin):
    bill_number = models.CharField(primary_key=False, default=bill_number, editable=False, unique=True, max_length = 1500)
    bill_amount = models.IntegerField(blank=True, null=True)
    product_key = models.ManyToManyField(ProductDescription, db_constraint=False)


    def get_update_url(self):
        return "/product/delete/"+str(self.pk)

    def get_delete_url(self):
        return redirect('dashboard')    
    

    def __str__(self) :
        return str(self.bill_number)


