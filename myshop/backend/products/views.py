from rest_framework import viewsets
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer
from django.shortcuts import render
import plotly.graph_objects as go
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductOrdersChartAPIView(APIView):
    def get(self, request):
        # Получаем количество заказов для каждого продукта
        products = Product.objects.annotate(
            order_count=Count('order')
        ).order_by('-order_count')
        
        product_names = [product.name for product in products]
        order_counts = [product.order_count for product in products]
        
        # Создаем график
        fig = go.Figure([go.Bar(x=product_names, y=order_counts)])
        fig.update_layout(
            title='Популярность продуктов',
            xaxis_title='Продукты',
            yaxis_title='Количество заказов'
        )
        
        chart = fig.to_html(full_html=False)
        return Response({'chart': chart})

def charts_view(request):
    # Получаем данные для графика
    products = Product.objects.annotate(
        order_count=Count('order')
    ).order_by('-order_count')
    
    product_names = [product.name for product in products]
    order_counts = [product.order_count for product in products]
    
    # Создаем график
    fig = go.Figure([go.Bar(x=product_names, y=order_counts)])
    fig.update_layout(
        title='Популярность продуктов',
        xaxis_title='Продукты',
        yaxis_title='Количество заказов'
    )
    
    chart = fig.to_html(full_html=False)
    
    return render(request, 'charts.html', {'chart': chart})