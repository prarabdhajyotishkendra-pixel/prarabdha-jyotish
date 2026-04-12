from django import template
from astrology.models import PalmReading, Kundali
from django.utils import timezone

register = template.Library()

@register.simple_tag
def get_dashboard_stats():
    now = timezone.now()
    
    palm_total = PalmReading.objects.count()
    palm_today = PalmReading.objects.filter(created_at__date=now.date()).count()
    palm_month = PalmReading.objects.filter(created_at__year=now.year, created_at__month=now.month).count()
    
    kundali_total = Kundali.objects.count()
    kundali_today = Kundali.objects.filter(created_at__date=now.date()).count()
    kundali_month = Kundali.objects.filter(created_at__year=now.year, created_at__month=now.month).count()
    
    return {
        'palm_total': palm_total,
        'palm_today': palm_today,
        'palm_month': palm_month,
        'kundali_total': kundali_total,
        'kundali_today': kundali_today,
        'kundali_month': kundali_month,
        'overall_total': palm_total + kundali_total,
        'overall_today': palm_today + kundali_today
    }
