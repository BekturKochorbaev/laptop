import django_filters
from .models import *


class LaptopFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    screen_size = django_filters.NumberFilter(field_name='name')
    cpu_model = django_filters.CharFilter(field_name='cpu_model', lookup_expr='icontains')
    ram_size_gb = django_filters.NumberFilter(field_name='cpu_model', lookup_expr='icontains')
    gpu_model = django_filters.CharFilter(field_name='gpu_model', lookup_expr='icontains')
    storage_size_gb = django_filters.NumberFilter(field_name='gpu_model', lookup_expr='icontains')
    operation_system = django_filters.CharFilter(field_name='operation_system', lookup_expr='icontains')

    class Meta:
        model = Laptop
        fields = ['name', 'screen_size', 'cpu_model', 'ram_size_gb', 'gpu_model', 'storage_size_gb', 'operation_system']
