from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserProfileSerializer
from rest_framework import permissions
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from inventory_mgmt.decorators import check_user_auth


@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def login(request):
    errors = []
    if request.method == "GET":
        user_serializer = UserProfileSerializer()

    if request.method == "POST":
        user_serializer = UserProfileSerializer(data=request.data)
        try:
            user = user_serializer.user_login(request.POST.get('username'), request.POST.get('password'))
            print user
            request.user = user
            request.session['email'] = user.email
            return redirect('inventory_list')
        except Exception as e:
            errors.append(e)

    return render(request, 'login.html', {'serializer': user_serializer, 'errors': errors})


@check_user_auth
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def user_logout(request):
    del request.session['email']
    return HttpResponseRedirect(reverse('login'))
