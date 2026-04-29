"""
URL configuration for prarabdha_jyotish project.
Final Professional Version with Custom Admin Support
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Hum apne custom admin site ko yahan import kar rahe hain jise humne admin.py mein banaya hai
from astrology.admin import custom_admin_site 

urlpatterns = [
    # 1. Custom Professional Admin Dashboard
    path('admin/', custom_admin_site.urls),
    
    # 2. Astrology App ki saari URLs (Home, Hastarekha, Kundali, Success)
    path('', include('astrology.urls')),
]

# 3. STATIC & MEDIA FILES SETUP
if settings.DEBUG:
    # Media Files (Clients ki uploaded Palm Photos ke liye)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Note: Humne yahan se STATIC_URL wala code hata diya hai kyunki 
    # django.contrib.staticfiles automatically STATICFILES_DIRS (static folder) se 
    # files serve kar deta hai jab DEBUG=True hota hai.

# Final Header Customization (Safe Side)
admin.site.site_header = "Prarabdha Jyotish Kendra Admin"
admin.site.site_title = "Astrology Portal"
admin.site.index_title = "Welcome to Business Analytics"