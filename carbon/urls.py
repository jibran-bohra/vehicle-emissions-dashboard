from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
        path('', views.ToyotaModelListView.as_view(), name= 'view-emission'),
]