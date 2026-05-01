import urllib.parse
from django.shortcuts import redirect, render
import datetime
from django.views.generic import TemplateView, CreateView
from .models import PalmReading, Kundali
from .forms import PalmReadingForm, KundaliForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import json
import os
import google.generativeai as genai
from django.http import JsonResponse
from django.views import View
from django.contrib.auth import logout

def admin_logout_view(request):
    logout(request)
    return redirect('/')

def dynamic_rashifal_view(request, zodiac_sign):
    current_date = datetime.date.today()
    try:
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDbTeJhS6KDPhkjRaPvvKpKY3SDLsCQPZ0")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = f"Provide a detailed daily horoscope for {zodiac_sign} for {current_date} in Hindi. Cover health, career, and love life."
        
        response = model.generate_content(prompt)
        horoscope_text = response.text
    except Exception as e:
        horoscope_text = "Rashifal generation failed. Please try again later."
        
    context = {
        'zodiac_sign': zodiac_sign,
        'current_date': current_date,
        'horoscope_text': horoscope_text
    }
    return render(request, 'rashifal_detail.html', context)

class HomeView(TemplateView):
    template_name = 'home.html'

class ChatView(TemplateView):
    template_name = 'chat.html'

class HastarekhaCreateView(CreateView):
    model = PalmReading
    form_class = PalmReadingForm
    template_name = 'hastarekha_form.html'
    
    def form_valid(self, form):
        self.object = form.save()
        
        image_url = ""
        if self.object.image:
            image_url = self.request.build_absolute_uri(self.object.image.url)
            
        message = f"*NAMASTE PRARABDHA JYOTISH!* 🕉️\n\nI want a *Palm Reading*.\n\n*CLIENT DETAILS:*\n• Name: {self.object.name}\n• Phone: {self.object.phone}\n• Amount: ₹251\n\n*VIEW HAND PHOTO:*\n\n{image_url}\n\n_System Note: Payment done and Hand Image uploaded successfully._"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/916267357802?text={encoded_message}"
        
        return redirect(whatsapp_url)

class KundaliCreateView(CreateView):
    model = Kundali
    form_class = KundaliForm
    template_name = 'kundali_form.html'
    
    def form_valid(self, form):
        self.object = form.save()
        
        message = f"*NAMASTE PRARABDHA JYOTISH!* 🕉️\n\nI want a *Full Kundali Check*.\n\n*CLIENT DETAILS:*\n• Name: {self.object.name}\n• DOB: {self.object.dob}\n• Time: {self.object.birth_time}\n• Place: {self.object.birth_place}\n• Phone: {self.object.phone}\n• Amount: ₹751\n\n_System Note: Payment done and details saved successfully._"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/916267357802?text={encoded_message}"
        
        return redirect(whatsapp_url)

class SuccessView(TemplateView):
    template_name = 'success.html'

def track_status(request):
    status_message = None
    phone_number = None

    if request.method == 'POST':
        phone = request.POST.get('phone', '').strip()
        if phone:
            phone_number = phone
            status_message = "Your consultation is currently 'In Progress'. Our astrologers are analyzing your details. You will receive a WhatsApp message shortly."
        else:
            status_message = "Please enter a valid mobile number."

    context = {
        'status_message': status_message,
        'phone_number': phone_number
    }
    return render(request, 'track_status.html', context)

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def post(self, request, *args, **kwargs):
        user_email = request.POST.get('user_email')
        message = request.POST.get('message')
        
        if user_email and message:
            subject = f"New Astrology Inquiry from {user_email}"
            body = f"Sender: {user_email}\n\nMessage:\n{message}"
            
            try:
                # Send email using Django SMTP
                send_mail(
                    subject=subject,
                    message=body,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=['prarabdhajyotishkendra@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully. We will connect with you soon.")
            except Exception as e:
                # DEBUGGING: Print the exact raw error to the terminal
                print(f"\n================ SMTP ERROR ================")
                print(f"Error Type: {type(e).__name__}")
                print(f"Error Message: {e}")
                print(f"============================================\n")
                
                messages.error(request, "There was an error sending your message. Please try again later.")
        else:
            messages.error(request, "Please provide both your email and a message.")
            
        return redirect('contact')

class AstroGPTAPIView(View):
    def post(self, request, *args, **kwargs):
        try:
            # 1. Session Tracking Logic (Limit: 7th message cuts off)
            count = request.session.get('astro_chat_count', 0)
            if count >= 6:
                return JsonResponse({'redirect': True, 'message': 'Cosmic energy exhausted. Please book a full session.'})
                
            request.session['astro_chat_count'] = count + 1
            request.session.modified = True
            
            # 2. Extract Message
            data = json.loads(request.body)
            message = data.get('message', '')
            
            # 3. Gemini Configuration
            api_key = os.getenv("GEMINI_API_KEY", "AIzaSyDbTeJhS6KDPhkjRaPvvKpKY3SDLsCQPZ0")
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"""
            You are AstroGPT, a professional and wise Vedic Astrologer. 
            You must ONLY answer questions related to Career, Life, Marriage (Love/Arrange), Job, and Future Planning using astrological wisdom.
            If the user asks a non-astrology question (like programming, math, general knowledge, sports, etc.), you MUST reply exactly with: 
            "I can only guide you through the wisdom of the stars."
            Keep your answers concise, mystical, and empathetic. 
            
            User's question: {message}
            """
            
            response = model.generate_content(prompt)
            return JsonResponse({'redirect': False, 'reply': response.text})
            
        except Exception as e:
            return JsonResponse({'redirect': False, 'reply': 'The cosmic energies are currently shifting. Please try again later.'})
