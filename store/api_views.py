from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, OrderSerializer
from .views import get_user_order

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_products(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    products = Product.objects.all()
    if query:
        products = product.filter(name__icontains=query)
    if category_id:
        products = products.filter(category_id=category_id)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_order(request):
    order = get_user_order(request.user)
    serializer = OrderSerializer(order)
    return Response(serializer.data)
