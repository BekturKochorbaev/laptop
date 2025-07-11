from django.contrib import admin
from .models import LaptopImage, Laptop, ContactNumber, Contact, AboutUs, Warranty, Delivery


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


class ContactAdmin(admin.ModelAdmin):
    inlines = [ContactNumberInline]


admin.site.register(Contact, ContactAdmin)
admin.site.register(AboutUs)
admin.site.register(Delivery)
admin.site.register(Warranty)
