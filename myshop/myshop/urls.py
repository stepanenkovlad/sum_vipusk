from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, OrderViewSet
from django.contrib import admin  # Добавьте эту строку

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
