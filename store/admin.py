from django.contrib import admin
from .models import LaptopImage, Laptop, ContactNumber, Contact, AboutUs, Warranty, Delivery, Order, ServiceCallback, \
    ContactWhatsApp, ContactTelegram, ContactInstagram, Service, PrinterImage, Printer


class LaptopImageInline(admin.TabularInline):
    model = LaptopImage
    extra = 0


class LaptopAdmin(admin.ModelAdmin):
    inlines = [LaptopImageInline]
    list_display = ['name', 'ram_size_gb', 'cpu_model', 'articles', 'price']
    search_fields = ('articles', 'name')
    list_filter = ('in_stock', 'screen_size', 'ram_size_gb', 'storage_size_gb')
    exclude = ('slug', 'types')


admin.site.register(Laptop, LaptopAdmin)


class PrinterImageInline(admin.TabularInline):
    model = PrinterImage
    extra = 0


class PrinterAdmin(admin.ModelAdmin):
    inlines = [PrinterImageInline]
    list_display = ['name', 'price']
    exclude = ('slug', 'types')


admin.site.register(Printer, PrinterAdmin)


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
admin.site.register(Service)
