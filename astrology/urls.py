from django.urls import path
from .views import HomeView, HastarekhaCreateView, KundaliCreateView, SuccessView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('hastarekha/', HastarekhaCreateView.as_view(), name='hastarekha'),
    path('kundali/', KundaliCreateView.as_view(), name='kundali'),
    path('success/', SuccessView.as_view(), name='success'),
]
