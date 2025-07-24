from django.urls import path, include

from store.views import LaptopListApiView, LaptopDetailApiView, ContactListApiView, AboutUsListApiView, \
    WarrantyListApiView, OrderCreateApiView, CartViewSet, CartItemViewSet, DeliveryListApiView, ServiceListApiView, \
    ServiceCallbackCreateApiView, CallbackCreateApiView

urlpatterns = [
    path('laptop/', LaptopListApiView.as_view()),
    path('laptop/<int:pk>/', LaptopDetailApiView.as_view()),
    path('contact/', ContactListApiView.as_view()),
    path('aboutus/', AboutUsListApiView.as_view()),
    path('delivery/', DeliveryListApiView.as_view()),
    path('warranty/', WarrantyListApiView.as_view()),
    path('service/', ServiceListApiView.as_view()),
    path('order/', OrderCreateApiView.as_view()),
    path('service-callback/', ServiceCallbackCreateApiView.as_view()),
    path('callback/', CallbackCreateApiView.as_view()),

    path('cart/', CartViewSet.as_view({'get': 'retrieve'}), name='cart_detail'),

    path('cart_items/', CartItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='car-item_list'),
    path('cart_items/<int:pk>/', CartItemViewSet.as_view({'put': 'update', 'delete': 'destroy'})),
]

