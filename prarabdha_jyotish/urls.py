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
from astrology.views import admin_logout_view

urlpatterns = [
    # Force Fix for Django 5.x Admin Logout HTTP 405 error (uses custom GET view)
    path('admin/logout/', admin_logout_view, name='admin_logout'),
    
    # 1. Custom Professional Admin Dashboard
    path('admin/', custom_admin_site.urls),
    
    # 2. Astrology App ki saari URLs (Home, Hastarekha, Kundali, Success)
    path('', include('astrology.urls')),
]

# 3. STATIC & MEDIA FILES SETUP
# Media Files (Clients ki uploaded Palm Photos ke liye)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Final Header Customization (Safe Side)
admin.site.site_header = "Prarabdha Jyotish Kendra Admin"
admin.site.site_title = "Astrology Portal"
admin.site.index_title = "Welcome to Business Analytics"