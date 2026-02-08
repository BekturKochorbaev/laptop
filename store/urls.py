from django.urls import path
from store.views import LaptopListApiView, LaptopDetailApiView, ContactListApiView, AboutUsListApiView, \
    WarrantyListApiView, OrderCreateApiView, CartViewSet, DeliveryListApiView, ServiceListApiView, \
    ServiceCallbackCreateApiView, CallbackCreateApiView, CartCallbackView, PrinterListApiView, PrinterDetailApiView, \
    LaptopCartItemViewSet, PrinterCartItemViewSet

urlpatterns = [
    path('laptop/', LaptopListApiView.as_view()),
    path('laptop/<str:slug>/', LaptopDetailApiView.as_view()),
    path('printer/', PrinterListApiView.as_view()),
    path('printer/<str:slug>/', PrinterDetailApiView.as_view()),
    path('contact/', ContactListApiView.as_view()),
    path('aboutus/', AboutUsListApiView.as_view()),
    path('delivery/', DeliveryListApiView.as_view()),
    path('warranty/', WarrantyListApiView.as_view()),
    path('service/', ServiceListApiView.as_view()),
    path('order/', OrderCreateApiView.as_view()),
    path('service-callback/', ServiceCallbackCreateApiView.as_view()),
    path('callback/', CallbackCreateApiView.as_view()),
    path('cart-callback/', CartCallbackView.as_view()),

    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_detail'),

    path('laptop_cart_items/', LaptopCartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='car-item_list'),
    path('laptop_cart_items/<str:slug>/', LaptopCartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
    path('printer_cart_items/', PrinterCartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='car-item_list'),
    path('printer_cart_items/<str:slug>/', PrinterCartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

]

