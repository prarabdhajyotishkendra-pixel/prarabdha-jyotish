from django.contrib import admin
from .models import PalmReading, Kundali

@admin.register(PalmReading)
class PalmReadingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Kundali)
class KundaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'dob', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
