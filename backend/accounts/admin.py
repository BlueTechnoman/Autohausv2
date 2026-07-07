from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # ← das ist der Schlüssel!
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Zeigt die extra "role"-Spalte in der Übersicht
    list_display = ["username", "email", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff"]

    # Fügt das "role"-Feld zu den Bearbeitungsmasken hinzu
    fieldsets = UserAdmin.fieldsets + (
        ("Rolle", {"fields": ("role",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Rolle", {"fields": ("role",)}),
    )