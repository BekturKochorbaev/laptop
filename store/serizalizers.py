from rest_framework import serializers
from store.models import Laptop, LaptopImage, Contact, ContactNumber, Order, CartItem, Cart, AboutUs, Warranty, \
    Delivery, Service, ServiceCallback, ContactWhatsApp, ContactTelegram, ContactInstagram, Callback
from .services import send_to_telegram, send_to_telegram_service, send_to_telegram_callback


class LaptopImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = LaptopImage
        fields = ['id', 'image']


class LaptopListSerializers(serializers.ModelSerializer):
    laptop_image = LaptopImageSerializers(read_only=True, many=True)
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Laptop
        fields = ['id', 'name', 'discount', 'discount_price', 'in_stock', 'in_composition', 'articles', 'screen_size', 'ram_size_gb', 'cpu_model', 'brand', 'gpu_model',
                  'operating_system', 'storage_size_gb', 'laptop_image', 'price']

    def get_discount_price(self, obj):
        return obj.get_discount_price()


class LaptopDetailSerializers(serializers.ModelSerializer):
    laptop_image = LaptopImageSerializers(read_only=True, many=True)

    class Meta:
        model = Laptop
        fields = '__all__'


class ContactNumberSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactNumber
        fields = ['id', 'phone_number']


class ContactWhatsAppSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactWhatsApp
        fields = ['id', 'whatsapp']


class ContactTelegramSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactTelegram
        fields = ['id', 'telegram']


class ContactInstagramSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactInstagram
        fields = ['id', 'instagram']


class ContactSerializers(serializers.ModelSerializer):
    phone_number = ContactNumberSerializers(read_only=True, many=True)
    whatsapp = ContactWhatsAppSerializers(read_only=True, many=True)
    telegram = ContactTelegramSerializers(read_only=True, many=True)
    instagram = ContactInstagramSerializers(read_only=True, many=True)

    class Meta:
        model = Contact
        fields = ['id', 'address', 'work_schedule', 'phone_number', 'whatsapp', 'telegram', 'instagram']


class AboutUsSerializers(serializers.ModelSerializer):

    class Meta:
        model = AboutUs
        fields = '__all__'


class DeliverySerializers(serializers.ModelSerializer):

    class Meta:
        model = Delivery
        fields = '__all__'


class WarrantySerializers(serializers.ModelSerializer):

    class Meta:
        model = Warranty
        fields = '__all__'


class ServiceSerializers(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['link', 'phone_number', 'full_name', 'description']

    def create(self, validated_data):
        callback = Order.objects.create(**validated_data)
        send_to_telegram(validated_data)
        return callback


class ServiceCallbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = ServiceCallback
        fields = ['phone_number', 'full_name', 'description']

    def create(self, validated_data):
        callback = ServiceCallback.objects.create(**validated_data)
        send_to_telegram_service(validated_data)
        return callback


class CallbackSerializers(serializers.ModelSerializer):
    class Meta:
        model = Callback
        fields = ['phone_number', 'full_name', 'description']

    def create(self, validated_data):
        callback = Callback.objects.create(**validated_data)
        send_to_telegram_callback(validated_data)
        return callback


class CartItemDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_id(self, value):
        if not Laptop.objects.filter(id=value).exists():
            raise serializers.ValidationError("Продукт с таким ID не найден.")
        return value


class CallbackCreateSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=50)
    full_name = serializers.CharField(max_length=150)
    description = serializers.CharField(required=False, allow_blank=True)
    total_sum = serializers.IntegerField(allow_null=True)
    products = CartItemDetailSerializer(many=True)


class CartItemSerializer(serializers.ModelSerializer):
    product = LaptopListSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Laptop.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


