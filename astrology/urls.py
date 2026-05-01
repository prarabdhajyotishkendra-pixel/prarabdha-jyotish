from django.urls import path
from .views import HomeView, ChatView, HastarekhaCreateView, KundaliCreateView, SuccessView, AstroGPTAPIView, ContactView
from . import views
from .api import PalmReadingAPIView, KundaliAPIView, CheckReportAPIView

urlpatterns = [
    # Web HTML Routes
    path('', HomeView.as_view(), name='home'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('hastarekha/', HastarekhaCreateView.as_view(), name='hastarekha'),
    path('kundali/', KundaliCreateView.as_view(), name='kundali'),
    path('success/', SuccessView.as_view(), name='success'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('track-status/', views.track_status, name='track_status'),
    
    # API Routes
    path('api/chat/', AstroGPTAPIView.as_view(), name='api_chat'),
    path('api/palm-reading/', PalmReadingAPIView.as_view(), name='api_palm_reading'),
    path('api/kundali/', KundaliAPIView.as_view(), name='api_kundali'),
    path('api/check-report/', CheckReportAPIView.as_view(), name='api_check_report'),
]
