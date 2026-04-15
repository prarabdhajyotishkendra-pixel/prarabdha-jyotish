from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import PalmReading, Kundali
from .forms import PalmReadingForm, KundaliForm

@method_decorator(csrf_exempt, name='dispatch')
class PalmReadingAPIView(View):
    def post(self, request, *args, **kwargs):
        form = PalmReadingForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({
                "success": True, 
                "id": obj.id, 
                "message": "Palm Reading submitted successfully."
            })
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class KundaliAPIView(View):
    def post(self, request, *args, **kwargs):
        form = KundaliForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return JsonResponse({
                "success": True, 
                "id": obj.id, 
                "message": "Horoscope submitted successfully."
            })
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CheckReportAPIView(View):
    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone', '').strip()
        if not phone:
            return JsonResponse({"success": False, "error": "Phone parameter is required."}, status=400)
            
        palms = PalmReading.objects.filter(phone=phone).order_by('-created_at')
        kundalis = Kundali.objects.filter(phone=phone).order_by('-created_at')
        
        palm_list = [{
            "id": p.id, 
            "name": p.name, 
            "payment_status": p.payment_status, 
            "status": p.status, 
            "report": p.report,
            "created_at": p.created_at.isoformat()
        } for p in palms]
        
        kundali_list = [{
            "id": k.id, 
            "name": k.name, 
            "payment_status": k.payment_status, 
            "status": k.status, 
            "report": k.report,
            "created_at": k.created_at.isoformat()
        } for k in kundalis]
        
        return JsonResponse({
            "success": True,
            "data": {
                "palm_requests": palm_list,
                "kundali_requests": kundali_list
            }
        })
