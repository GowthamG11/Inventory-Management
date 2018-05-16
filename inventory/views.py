from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .models import Inventory
from .serializers import InventorySerializer
import json
from django.http import HttpResponse, HttpResponseBadRequest
from userprofile.models import UserProfile
from inventory_mgmt.decorators import check_user_auth


@check_user_auth
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def inventory_list(request):
    role = ''
    if request.session.get('email'):
        try:
            userprofile = UserProfile.objects.get(email=request.session.get('email'))
            if userprofile:
                if 'Store Assistant' in userprofile.userroles.all().values_list('role__title', flat=True):
                    role = 'Store Assistant'
                else:
                    role = 'Store Manager'
        except UserProfile.DoesNotExist:
            pass
    inventory_qs = Inventory.objects.get_queryset()
    return render(request, 'inventory_list.html', {'inventories': inventory_qs, 'role': role})


@check_user_auth
@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def inventory_create(request):

    if request.method == 'GET':
        inventory_serializer = InventorySerializer()

    if request.method == 'POST':
        status = 'approved'
        if request.session.get('email'):
            try:
                userprofile = UserProfile.objects.get(email=request.session.get('email'))
                if userprofile:
                    if 'Store Assistant' in userprofile.userroles.all().values_list('role__title', flat=True):
                        status = 'pending'
            except UserProfile.DoesNotExist:
                pass
        data = request.data
        inventory_serializer = InventorySerializer(data=data, context={'status': status})
        if inventory_serializer.is_valid():
            inventory_serializer.save()
            return redirect('inventory_list')
        else:
            if request.is_ajax():
                # Prepare JSON for parsing
                errors_dict = {}
                if inventory_serializer.errors:
                    for error in inventory_serializer.errors:
                        e = inventory_serializer.errors[error]
                        errors_dict[error] = unicode(e)

                return HttpResponseBadRequest(json.dumps(errors_dict))
            else:
                pass

    return render(request, 'create_inventory.html', {'serializer': inventory_serializer})


@check_user_auth
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def filter_inventory(request):

    filter_val = request.GET.get('filter_val', '')
    inventory_qs = None
    if filter_val:
        if filter_val == 'pending':
            inventory_qs = Inventory.objects.get_pending()
        elif filter_val == 'approved':
            inventory_qs = Inventory.objects.get_approved()
        elif filter_val == 'all':
            inventory_qs = Inventory.objects.get_queryset()
    inventory_serializer = InventorySerializer(inventory_qs, many=True, add_field='status',)
    print inventory_serializer.data
    return HttpResponse(json.dumps(inventory_serializer.data))


@check_user_auth
def inventory_approve(request, pk):

    try:
        inventory_obj = Inventory.objects.get(pk=pk)
        inventory_obj.status = 'approved'
        inventory_obj.save()
    except Inventory.DoesNotExist:
        pass
    return redirect('inventory_list')
