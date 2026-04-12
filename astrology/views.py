from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy
from .models import PalmReading, Kundali
from .forms import PalmReadingForm, KundaliForm

class HomeView(TemplateView):
    template_name = 'home.html'

class HastarekhaCreateView(CreateView):
    model = PalmReading
    form_class = PalmReadingForm
    template_name = 'hastarekha_form.html'
    success_url = reverse_lazy('success')

class KundaliCreateView(CreateView):
    model = Kundali
    form_class = KundaliForm
    template_name = 'kundali_form.html'
    success_url = reverse_lazy('success')

class SuccessView(TemplateView):
    template_name = 'success.html'

