from django.db import models
from accounts.models import UserProfile
from phonenumber_field.modelfields import PhoneNumberField
from django_ckeditor_5.fields import CKEditor5Field


class Laptop(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название")
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')
    link = models.URLField(verbose_name='Ссылка на ноутбук', null=True, blank=True)
    price = models.IntegerField(verbose_name="Цена")
    in_stock = models.BooleanField(default=False, verbose_name='В Наличии')
    discount = models.PositiveSmallIntegerField(verbose_name='Скидка %', null=True, blank=True)
    warranty = models.PositiveSmallIntegerField(default=3, verbose_name='Гарантия')
    brand = models.CharField(max_length=250, verbose_name='Бренд', null=True)

    screen_size = models.FloatField(verbose_name="Размер экрана (дюймы)")
    screen_type = models.CharField(max_length=150, verbose_name="Тип экрана")
    resolution = models.CharField(max_length=150, verbose_name="Разрешение экрана")
    refresh_rate = models.PositiveSmallIntegerField(default=60, verbose_name="Частота обновления (Гц)")
    operating_system = models.CharField(max_length=150, choices=[
                                                                ('Windows 10', 'Windows 10'),
                                                                ('Windows 11', 'Windows 11'),
                                                                ('Ubuntu', 'Ubuntu'),
                                                                ('MacOS', 'MacOS'),
                                                                 ],
                                        blank=True, null=True, verbose_name="Операционная система")

    # Память
    ram_size_gb = models.PositiveSmallIntegerField(verbose_name="Оперативная память (ГБ)")
    storage_size_gb = models.PositiveSmallIntegerField(verbose_name="Объем SSD (ГБ)")
    storage_type = models.CharField(max_length=150, default="SSD NVMe", verbose_name="Тип накопителя")

    # Процессор
    cpu_model = models.CharField(max_length=150, verbose_name="Модель процессора")
    cpu_cores = models.PositiveSmallIntegerField(verbose_name="Количество ядер")
    cpu_threads = models.PositiveSmallIntegerField(verbose_name="Количество потоков")
    cpu_frequency_mhz = models.PositiveIntegerField(verbose_name="Макс. частота процессора (МГц)")
    cpu_cache_mb = models.PositiveSmallIntegerField(verbose_name="Кэш процессора (МБ)")

    # Видеокарта
    gpu_model = models.CharField(max_length=150, verbose_name="Модель видеокарты")
    gpu_memory = models.CharField(max_length=150, verbose_name="Объем видеопамяти")

    # Сети
    wifi = models.CharField(max_length=150, verbose_name="Wi-Fi")
    ethernet = models.BooleanField(default=False, verbose_name="Ethernet")
    bluetooth = models.BooleanField(default=False, verbose_name="Bluetooth")

    # Порты
    usb_type_a_count = models.PositiveSmallIntegerField(default=0, verbose_name="USB Type-C (шт)")
    hdmi_count = models.BooleanField(default=False, verbose_name="HDMI")
    ethernet_port = models.BooleanField(default=False, verbose_name="Ethernet-порт")
    audio_jack = models.BooleanField(default=True, verbose_name="Аудиоразъём")

    # Дополнительно
    keyboard_backlight = models.BooleanField(default=False, verbose_name="Подсветка клавиатуры")
    battery_type = models.CharField(max_length=150, verbose_name="Тип аккумулятора")
    battery_capacity_wh = models.FloatField(verbose_name="Емкость аккумулятора (Вт·ч)")
    operation_system = models.CharField(max_length=150, verbose_name='Операционная система')

    # Габариты
    width_mm = models.FloatField(verbose_name="Ширина (мм)")
    thickness_mm = models.FloatField(verbose_name="Толщина (мм)")
    weight_kg = models.FloatField(verbose_name="Вес (кг)")

    class Meta:
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбук'

    def __str__(self):
        return f'{self.name}-{self.price}'


class LaptopImage(models.Model):
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE, related_name='laptop_image')
    image = models.FileField(upload_to='laptop_images', null=True, blank=True)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображение'


class Contact(models.Model):
    address = models.CharField(max_length=650)
    work_schedule = CKEditor5Field(verbose_name='График работы:', config_name='extends')
    email = models.EmailField(verbose_name='Email')

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return f'{self.address}-{self.email}'


class ContactNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='phone_number')
    phone_number = PhoneNumberField(region=None, null=True, blank=True, verbose_name='Телефон номер', default='+996779311921')

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номер'

    def __str__(self):
        return f'{self.contact}'


class ContactWhatsApp(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='whatsapp')
    whatsapp = models.URLField(null=True, blank=True, verbose_name='Ссылка на WatsApp', default='https://wa.me/996771222333')

    class Meta:
        verbose_name = 'WhatsApp'
        verbose_name_plural = 'WhatsApp'

    def __str__(self):
        return f'{self.contact}'


class ContactTelegram(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='telegram')
    telegram = models.URLField(null=True, blank=True, verbose_name='Ссылка на Telegram')

    class Meta:
        verbose_name = 'Telegram'
        verbose_name_plural = 'Telegram'

    def __str__(self):
        return f'{self.contact}'


class ContactInstagram(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='instagram')
    instagram = models.URLField(null=True, blank=True, verbose_name='Ссылка на Instagram')

    class Meta:
        verbose_name = 'Instagram'
        verbose_name_plural = 'Instagram'

    def __str__(self):
        return f'{self.contact}'


class Order(models.Model):
    link = models.URLField(null=True, blank=True)
    phone_number = models.CharField(max_length=50,null=True, blank=True, verbose_name='Тел. ном')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Заказы'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.laptop}-{self.full_name}-{self.email}'


class ServiceCallback(models.Model):
    phone_number = models.CharField(max_length=50, verbose_name='Тел. ном')
    full_name = models.CharField(max_length=150)
    email = models.EmailField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на сервис'
        verbose_name_plural = 'Заявка на сервис'

    def __str__(self):
        return f'{self.laptop}-{self.full_name}-{self.email}'


class AboutUs(models.Model):
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')

    class Meta:
        verbose_name = 'О Нас'
        verbose_name_plural = 'О Нас'


class Delivery(models.Model):
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставка'


class Warranty(models.Model):
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')

    class Meta:
        verbose_name = 'Гарантия'
        verbose_name_plural = 'Гарантия'


class Service(models.Model):
    description = CKEditor5Field(verbose_name='Описание', config_name='extends')

    class Meta:
        verbose_name = 'Сервис и обслуживание'
        verbose_name_plural = 'Сервис и обслуживание'


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def get_total_price(self):
        return self.product.price * self.quantity