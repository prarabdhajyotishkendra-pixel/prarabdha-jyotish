from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, View
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

class CheckReportView(View):
    def get(self, request):
        return render(request, 'check_report.html')

    def post(self, request):
        phone = request.POST.get('phone', '').strip()
        context = {'searched': True, 'phone': phone}
        if phone:
            context['palm_requests'] = PalmReading.objects.filter(phone=phone).order_by('-created_at')
            context['kundali_requests'] = Kundali.objects.filter(phone=phone).order_by('-created_at')
        else:
            context['error'] = 'Please enter a valid phone number.'
            context['searched'] = False
        
        return render(request, 'check_report.html', context)
