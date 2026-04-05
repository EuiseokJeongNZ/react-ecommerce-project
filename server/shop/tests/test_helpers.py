from decimal import Decimal

from django.contrib.auth import get_user_model

from shop.models.product import Product
from shop.models.address import Address
from shop.models.order import Order, OrderItem

from decimal import Decimal

from django.contrib.auth import get_user_model

from shop.models.product import Product
from shop.models.address import Address
from shop.models.order import Order, OrderItem


User = get_user_model()

def create_user(
    email="test@example.com",
    password="testpass123",
    name="Test User",
    phone="02712345678",
    role="customer",
):
    return User.objects.create_user(
        email=email,
        password=password,
        name=name,
        phone=phone,
        role=role,
    )

def create_product(
    title="Test Product",
    final_price="29.99",
    stock=10,
    original_price=None,
    category="protein",
    brand="Test Brand",
    tag="normal",
    tagline="Test Tagline",
    info="Test product info",
    flavor="Vanilla",
    weight="1kg",
    serve="30 servings",
    is_active=True,
):
    return Product.objects.create(
        title=title,
        final_price=Decimal(final_price),
        original_price=Decimal(original_price) if original_price is not None else None,
        stock=stock,
        category=category,
        brand=brand,
        tag=tag,
        tagline=tagline,
        info=info,
        flavor=flavor,
        weight=weight,
        serve=serve,
        is_active=is_active,
    )

def create_address(
    user,
    recipient="Test User",
    phone="02712345678",
    zip="1234",
    addr1="test St, Auckland",
    addr2="Room 123",
    is_default=True,
):
    return Address.objects.create(
        user=user,
        recipient=recipient,
        phone=phone,
        zip=zip,
        addr1=addr1,
        addr2=addr2,
        is_default=is_default,
    )