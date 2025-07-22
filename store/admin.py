from django.contrib import admin
from .models import LaptopImage, Laptop, ContactNumber, Contact, AboutUs, Warranty, Delivery, Order, ServiceCallback, \
    ContactWhatsApp, ContactTelegram, ContactInstagram


class LaptopImageInline(admin.TabularInline):
    model = LaptopImage
    extra = 1


class LaptopAdmin(admin.ModelAdmin):
    inlines = [LaptopImageInline]
    list_display = ['name', 'ram_size_gb', 'cpu_model', 'price']


admin.site.register(Laptop, LaptopAdmin)


class ContactNumberInline(admin.TabularInline):
    model = ContactNumber
    extra = 1


class ContactWhatsAppInline(admin.TabularInline):
    model = ContactWhatsApp
    extra = 1


class ContactTelegramInline(admin.TabularInline):
    model = ContactTelegram
    extra = 1


class ContactInstagramInline(admin.TabularInline):
    model = ContactInstagram
    extra = 1


class ContactAdmin(admin.ModelAdmin):
    inlines = [ContactNumberInline, ContactWhatsAppInline, ContactTelegramInline, ContactInstagramInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(AboutUs)
admin.site.register(Delivery)
admin.site.register(Warranty)
admin.site.register(Order)
admin.site.register(ServiceCallback)
