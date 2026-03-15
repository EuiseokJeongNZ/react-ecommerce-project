# urls.py

from django.urls import path
from .views import product_views, auth_views, address_views, profile_views, order_views

urlpatterns = [
    path("health/", product_views.health),
    path("products/", product_views.product_list),
    path("auth/login/", auth_views.login),
    path("auth/me/", auth_views.me),
    path("auth/logout/", auth_views.logout),
    path("auth/refresh/", auth_views.refresh),
    path("auth/signup/", auth_views.signup),
    path("address/", address_views.address_list),
    path("address/<int:address_id>/", address_views.address_detail),
    path("profile/", profile_views.profile),
    path("orders/", order_views.order_list_create),
]
