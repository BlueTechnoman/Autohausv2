#Registriert Modelle im Django-Adminbereich und macht es verwendbar (RH, NW)

from django.contrib import admin
from .models import Vehicle, VehicleImage, PriceHistory


class VehicleImageInline(admin.TabularInline):
    model  = VehicleImage
    extra  = 1


class PriceHistoryInline(admin.TabularInline):
    model          = PriceHistory
    extra          = 0
    readonly_fields = ["recorded_at"]


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display  = ["brand", "model", "year", "mileage", "price", "status", "kraftstoff"]
    list_filter   = ["status", "kraftstoff", "getriebe", "brand"]
    search_fields = ["brand", "model", "farbe", "beschreibung"]
    inlines       = [VehicleImageInline, PriceHistoryInline]


@admin.register(VehicleImage)
class VehicleImageAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "uploaded_at"]


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display  = ["vehicle", "price", "recorded_at", "note"]
    readonly_fields = ["recorded_at"]