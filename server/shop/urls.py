from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health),
    path("products/", views.product_list),
]
