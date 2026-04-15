from django.contrib import admin
from django.utils import timezone
from .models import PalmReading, Kundali

class CustomAdminSite(admin.AdminSite):
    site_header = "Prarabdha Jyotish Kendra Admin"
    site_title = "Admin Portal"
    index_title = "Astrology Dashboard"
    index_template = "admin/custom_index.html"

    def index(self, request, extra_context=None):
        today = timezone.localtime().date()
        this_month = today.month
        
        palm_all = PalmReading.objects.count()
        palm_today = PalmReading.objects.filter(created_at__date=today).count()
        palm_month = PalmReading.objects.filter(created_at__month=this_month).count()
        
        kundali_all = Kundali.objects.count()
        kundali_today = Kundali.objects.filter(created_at__date=today).count()
        kundali_month = Kundali.objects.filter(created_at__month=this_month).count()

        extra_context = extra_context or {}
        extra_context.update({
            'total_requests': palm_all + kundali_all,
            'today_requests': palm_today + kundali_today,
            'month_requests': palm_month + kundali_month,
            
            'palm_all': palm_all,
            'palm_today': palm_today,
            'palm_month': palm_month,
            
            'kundali_all': kundali_all,
            'kundali_today': kundali_today,
            'kundali_month': kundali_month,
        })
        return super().index(request, extra_context=extra_context)

custom_admin_site = CustomAdminSite(name='custom_admin')

@admin.register(PalmReading, site=custom_admin_site)
class PalmReadingAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Kundali, site=custom_admin_site)
class KundaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'dob', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status')
    search_fields = ('name', 'phone')
    readonly_fields = ('created_at',)
