# urls.py

from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    path("health/", views.health),
    path("products/", views.product_list),
    path("auth/login/", auth_views.login),
    path("auth/me/", auth_views.me),
]
