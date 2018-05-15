from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('__all__')

    def user_login(self, username, password):

        try:
            user = UserProfile.objects.get(username=username, password=password)
        except UserProfile.DoesNotExist:
            msg = 'Please Enter Valid Login Credentials'
            raise Exception(msg)

        return user
