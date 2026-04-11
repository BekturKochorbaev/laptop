import django_filters
from .models import Laptop, Printer


class LaptopFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    screen_size = django_filters.CharFilter(field_name='screen_size', lookup_expr='icontains')
    cpu_model = django_filters.CharFilter(field_name='cpu_model', lookup_expr='icontains')
    ram_size_gb = django_filters.CharFilter(field_name='ram_size_gb', lookup_expr='icontains')
    gpu_model = django_filters.CharFilter(field_name='gpu_model', lookup_expr='icontains')
    storage_size_gb = django_filters.CharFilter(field_name='storage_size_gb', lookup_expr='icontains')
    operating_system = django_filters.CharFilter(field_name='operating_system', lookup_expr='icontains')

    class Meta:
        model = Laptop
        fields = ['name', 'screen_size', 'cpu_model', 'ram_size_gb', 'gpu_model', 'storage_size_gb', 'operating_system']


class PrinterListFilter(django_filters.FilterSet):
    class Meta:
        model = Printer
        fields = {'price': ['gt', 'lt'],
                  'created_date': ['gt', 'lt']
        }