from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from api.models import ApiUser, Storage, Product, Order
from api.serializers import UserSerializer, StorageSerializer, ProductSerializer, OrderSerializer


class UserModelViewSet(viewsets.ModelViewSet):
    queryset = ApiUser.objects.all()
    http_method_names = ['post', 'get', 'delete']
    serializer_class = UserSerializer

    authentication_classes = []
    permission_classes = []


class StorageModelViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

    @action(detail=True)
    def products(self, request, pk=None):
        products = Product.objects.select_related('storage').all().filter(storage=pk)
        # storage = get_object_or_404(Storage.objects.all(), id=pk)
        # products = storage.products
        return Response(
            ProductSerializer(products, many=True).data
        )

    @action(detail=True)
    def orders(self, request, pk=None):
        orders = Order.objects.select_related('storage', 'product').all().filter(storage=pk)
        # storage = get_object_or_404(Storage.objects.all(), id=pk)
        # orders = storage.order
        return Response(
            OrderSerializer(orders, many=True).data
        )


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('storage').all()
    serializer_class = ProductSerializer


class OrderModelViewSet(viewsets.ModelViewSet):
    # queryset = Order.objects.all().order_by('-date')[:5]
    queryset = Order.objects.select_related('storage', 'product')[:5]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user.type_user
        amount_product = int(request.data['amount_product'])
        storage = get_object_or_404(Storage.objects.all(), id=request.data['storage'])
        product = get_object_or_404(Product.objects.all(), id=request.data['product'])
        # check product in storage
        if product not in Product.objects.select_related('storage').all().filter(storage=storage):
            return Response(
                {'Error': f"Product '{product.name}' out of stock"}
            )
        # logic of provider_user
        if user == 'provider':
            order = Order.objects.create(
                amount_product=amount_product,
                storage=storage,
                product=product,
                type_order='supply'
            )
            order.save()
            product.amount += amount_product
            product.save()
            return Response(
                OrderSerializer(order).data
            )
        # logic of customer_user
        else:
            if product.amount < amount_product:
                return Response(
                    {'Error': f'Amount of product less {product.amount}'}
                )
            order = Order.objects.create(
                amount_product=amount_product,
                storage=storage,
                product=product,
                type_order='sending'
            )
            order.save()
            product.amount -= amount_product
            product.save()
            return Response(
                OrderSerializer(order).data
            )
