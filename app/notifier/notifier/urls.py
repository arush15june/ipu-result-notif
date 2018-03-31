from django.contrib import admin
from django.conf.urls import include, url


from fcm_django.api.rest_framework import FCMDeviceViewSet

urlpatterns = [
    url(r'^devices', FCMDeviceViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
    url(r'^admin/', admin.site.urls)
]
