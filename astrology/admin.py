from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import PalmReading, Kundali

class AstrologyAdminSite(admin.AdminSite):
    site_header = "Prarabdha Jyotish Kendra | Business Intelligence"
    site_title = "Admin Dashboard"
    index_title = "Astrology Analytics & Operations"
    index_template = "admin/index.html"

    def index(self, request, extra_context=None):
        from datetime import timedelta
        now = timezone.now()
        
        # Date boundaries
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        year_ago = now - timedelta(days=365)
        
        # Today
        today_p = PalmReading.objects.filter(created_at__date=now.date()).count()
        today_k = Kundali.objects.filter(created_at__date=now.date()).count()
        
        # Week
        week_p = PalmReading.objects.filter(created_at__gte=week_ago).count()
        week_k = Kundali.objects.filter(created_at__gte=week_ago).count()
        
        # Month
        month_p = PalmReading.objects.filter(created_at__gte=month_ago).count()
        month_k = Kundali.objects.filter(created_at__gte=month_ago).count()
        
        # Year
        year_p = PalmReading.objects.filter(created_at__gte=year_ago).count()
        year_k = Kundali.objects.filter(created_at__gte=year_ago).count()
        
        # Total
        total_p = PalmReading.objects.count()
        total_k = Kundali.objects.count()
        
        # Revenue Calculation Variables
        P_PRICE = 251
        K_PRICE = 751
        
        today_income = (today_p * P_PRICE) + (today_k * K_PRICE)
        week_income = (week_p * P_PRICE) + (week_k * K_PRICE)
        month_income = (month_p * P_PRICE) + (month_k * K_PRICE)
        year_income = (year_p * P_PRICE) + (year_k * K_PRICE)
        total_income = (total_p * P_PRICE) + (total_k * K_PRICE)

        extra_context = extra_context or {}
        extra_context.update({
            # Overview
            'today_income': today_income,
            'total_income': total_income,
            'total_p': total_p,
            'total_k': total_k,
            
            # Modal Detailed Breakdowns
            'today_p_income': today_p * P_PRICE,
            'today_k_income': today_k * K_PRICE,
            'today_p_count': today_p,
            'today_k_count': today_k,
            
            # Chart Data (JSON representation for Chart.js)
            'chart_data_labels': ['Today', 'Last 7 Days', 'Last 30 Days', 'Last Year', 'All Time'],
            'chart_data_palm': [today_p * P_PRICE, week_p * P_PRICE, month_p * P_PRICE, year_p * P_PRICE, total_p * P_PRICE],
            'chart_data_kundali': [today_k * K_PRICE, week_k * K_PRICE, month_k * K_PRICE, year_k * K_PRICE, total_k * K_PRICE],
        })
        
        return super().index(request, extra_context)

custom_admin_site = AstrologyAdminSite(name='custom_admin')

@admin.register(PalmReading, site=custom_admin_site)
class PalmReadingAdmin(admin.ModelAdmin):
    list_display = ('hand_image_preview', 'name', 'phone', 'amount', 'created_at')
    list_display_links = ('name',)
    readonly_fields = ('preview_large',)
    search_fields = ('name', 'phone')

    def amount(self, obj): 
        return "₹251"
    amount.short_description = "Revenue"

    def hand_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px; border: 1px solid #D4AF37;"/>'
                '</a>', 
                obj.image.url, obj.image.url
            )
        return format_html('<span style="color: #888;">No Image</span>')
    hand_image_preview.short_description = "Hand"

    def preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 500px; border-radius: 15px; border: 3px solid #D4AF37;"/>', obj.image.url)
        return "No Image"
    preview_large.short_description = "Full Image"

@admin.register(Kundali, site=custom_admin_site)
class KundaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'dob', 'birth_time', 'amount', 'created_at')
    search_fields = ('name', 'phone')
    
    def amount(self, obj): 
        return "₹751"
    amount.short_description = "Revenue"