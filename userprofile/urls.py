from django.conf.urls import url
from .views import login, user_logout

urlpatterns = [

    url(r'login/$', login, name='login'),
    url(r'logout/$', user_logout, name='logout'),

]