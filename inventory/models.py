from __future__ import unicode_literals

from django.db import models


STATUSES = (('approved', 'Approved'), ('pending', 'Pending'))


class InventoryManager(models.Manager):
    def get_queryset(self):
        return super(InventoryManager, self).get_queryset().all()

    def get_pending(self):
        return self.get_queryset().filter(status='pending')

    def get_approved(self):
        return self.get_queryset().filter(status='approved')


class Inventory(models.Model):

    product_id = models.IntegerField(unique=True)
    product_name = models.CharField(max_length=100, unique=True)
    vendor = models.CharField(max_length=100)
    mrp = models.CharField(max_length=20)
    batch_num = models.CharField(max_length=10)
    batch_date = models.DateField()
    qty = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUSES)

    objects = InventoryManager()

    def __str__(self):
        return self.product_name
