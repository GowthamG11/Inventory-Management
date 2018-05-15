from django.conf.urls import url
from .views import inventory_list, inventory_create, filter_inventory, inventory_approve


urlpatterns = [

    url(r'list/$', inventory_list, name='inventory_list'),
    url(r'create/$', inventory_create, name='inventory_create'),
    url(r'filter/$', filter_inventory, name='filter_inventory'),
    url(r'approve/(?P<pk>\d+)/$', inventory_approve, name='inventory_approve'),
]