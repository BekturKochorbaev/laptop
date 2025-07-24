from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .filters import LaptopFilter
from .models import Contact, AboutUs, Warranty
from .serizalizers import *
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class LaptopListApiView(ListAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_class = LaptopFilter

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Название", type=openapi.TYPE_STRING),
            openapi.Parameter('screen_size', openapi.IN_QUERY, description="Размер экрана", type=openapi.TYPE_NUMBER),
            openapi.Parameter('cpu_model', openapi.IN_QUERY, description="Процессор", type=openapi.TYPE_STRING),
            openapi.Parameter('ram_size_gb', openapi.IN_QUERY, description="ОЗУ (ГБ)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('gpu_model', openapi.IN_QUERY, description="Видеокарта", type=openapi.TYPE_STRING),
            openapi.Parameter('storage_size_gb', openapi.IN_QUERY, description="Память (ГБ)", type=openapi.TYPE_INTEGER),
            openapi.Parameter('operation_system', openapi.IN_QUERY, description="Операционная система", type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LaptopDetailApiView(RetrieveAPIView):
    queryset = Laptop.objects.all()
    serializer_class = LaptopDetailSerializers


class ContactListApiView(ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializers


class AboutUsListApiView(ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializers


class DeliveryListApiView(ListAPIView):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializers


class WarrantyListApiView(ListAPIView):
    queryset = Warranty.objects.all()
    serializer_class = WarrantySerializers


class ServiceListApiView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializers


class OrderCreateApiView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializers


class ServiceCallbackCreateApiView(CreateAPIView):
    queryset = ServiceCallback.objects.all()
    serializer_class = ServiceCallbackSerializers


class CallbackCreateApiView(CreateAPIView):
    queryset = Callback.objects.all()
    serializer_class = CallbackSerializers


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)







