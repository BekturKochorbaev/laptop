from rest_framework import serializers
from store.models import Laptop, LaptopImage, Contact, ContactNumber, Order, CartItem, Cart, AboutUs, Warranty, Delivery
from .services import send_to_telegram


class LaptopImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = LaptopImage
        fields = ['id', 'image']


class LaptopListSerializers(serializers.ModelSerializer):
    laptop_image = LaptopImageSerializers(read_only=True, many=True)

    class Meta:
        model = Laptop
        fields = ['name', 'screen_size', 'ram_size_gb', 'cpu_model', 'gpu_model', 'width_mm', 'height_mm',
                  'thickness_mm', 'weight_kg', 'laptop_image', 'price']


class LaptopDetailSerializers(serializers.ModelSerializer):
    laptop_image = LaptopImageSerializers(read_only=True, many=True)

    class Meta:
        model = Laptop
        fields = '__all__'


class ContactNumberSerializers(serializers.ModelSerializer):

    class Meta:
        model = ContactNumber
        fields = ['id', 'phone_number']


class ContactSerializers(serializers.ModelSerializer):
    phone_number = ContactNumberSerializers(read_only=True, many=True)

    class Meta:
        model = Contact
        fields = '__all__'


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


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['laptop', 'phone_number', 'full_name', 'email', 'description']

    def create(self, validated_data):
        callback = Order.objects.create(**validated_data)
        send_to_telegram(validated_data)
        return callback


class CartItemSerializer(serializers.ModelSerializer):
    product = LaptopListSerializers(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Laptop.objects.all(), write_only=True, source='product')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'get_total_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


