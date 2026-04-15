from django.urls import path
from .views import HomeView, HastarekhaCreateView, KundaliCreateView, SuccessView, CheckReportView
from .api import PalmReadingAPIView, KundaliAPIView, CheckReportAPIView

urlpatterns = [
    # Web HTML Routes
    path('', HomeView.as_view(), name='home'),
    path('hastarekha/', HastarekhaCreateView.as_view(), name='hastarekha'),
    path('kundali/', KundaliCreateView.as_view(), name='kundali'),
    path('success/', SuccessView.as_view(), name='success'),
    path('check-report/', CheckReportView.as_view(), name='check_report'),
    
    # API Routes
    path('api/palm-reading/', PalmReadingAPIView.as_view(), name='api_palm_reading'),
    path('api/kundali/', KundaliAPIView.as_view(), name='api_kundali'),
    path('api/check-report/', CheckReportAPIView.as_view(), name='api_check_report'),
]
