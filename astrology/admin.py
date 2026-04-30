from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import PalmReading, Kundali
import io
from django.http import HttpResponse

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
except ImportError:
    pass

@admin.action(description='Generate Premium PDF Report')
def generate_pdf_report(modeladmin, request, queryset):
    try:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        styles = getSampleStyleSheet()
        
        # Custom Premium Styles
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#D4AF37'), # Gold
            alignment=1, # Center
            spaceAfter=20
        )
        
        header_style = ParagraphStyle(
            'HeaderStyle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=10,
            spaceBefore=15
        )
        
        normal_style = ParagraphStyle(
            'NormalStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=12,
            textColor=colors.HexColor('#333333'),
            leading=16,
            spaceAfter=10
        )

        elements = []
        
        for idx, obj in enumerate(queryset):
            # 1. Header Section
            elements.append(Paragraph("Prarabdha Jyotish Kendra", title_style))
            elements.append(Paragraph("Astro-Spiritual Analysis & Reading", ParagraphStyle('SubTitle', parent=title_style, fontSize=14, textColor=colors.HexColor('#555555'))))
            elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#D4AF37'), spaceBefore=10, spaceAfter=20))
            
            # 2. Client Details
            elements.append(Paragraph("Client Details", header_style))
            service_type = "Hastarekha (Palm Reading)" if hasattr(obj, 'image') else "Sampoorna Kundali"
            
            details = f"<b>Name:</b> {obj.name}<br/>"
            details += f"<b>Phone:</b> {obj.phone}<br/>"
            details += f"<b>Service Requested:</b> {service_type}<br/>"
            
            if hasattr(obj, 'dob'):
                details += f"<b>Date of Birth:</b> {obj.dob}<br/>"
                details += f"<b>Birth Time:</b> {obj.birth_time}<br/>"
                details += f"<b>Birth Place:</b> {obj.birth_place}<br/>"
                
            elements.append(Paragraph(details, normal_style))
            elements.append(Spacer(1, 20))
            
            # 3. Analysis & Predictions
            elements.append(Paragraph("Analysis & Predictions", header_style))
            analysis_text = ("Based on the planetary positions and ancient Vedic principles, your cosmic energy "
                             "suggests a period of significant transformation. Trust your intuition as new paths "
                             "unfold. Professional growth and spiritual awareness are highly indicated in the coming cycle.")
            
            if obj.report:
                analysis_text = obj.report
                
            elements.append(Paragraph(analysis_text, normal_style))
            elements.append(Spacer(1, 20))
            
            # 4. Remedies
            elements.append(Paragraph("Divine Remedies", header_style))
            remedies_text = ("• Chant the Mahamrityunjaya Mantra 108 times daily.<br/>"
                             "• Offer water to Surya Dev (Sun God) every morning.<br/>"
                             "• Wear a gold or yellow thread on your right wrist for protection.")
            elements.append(Paragraph(remedies_text, normal_style))
            
            # Footer
            elements.append(Spacer(1, 40))
            elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CCCCCC'), spaceBefore=10, spaceAfter=10))
            elements.append(Paragraph("<i>May the divine light guide your path. 🕉️</i>", ParagraphStyle('Footer', parent=normal_style, alignment=1, textColor=colors.HexColor('#888888'))))
            
            if idx < len(queryset) - 1:
                elements.append(PageBreak())

        doc.build(elements)
        buffer.seek(0)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        filename = "Astrology_Report.pdf" if queryset.count() > 1 else f"Report_{queryset.first().name.replace(' ', '_')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except NameError:
        # ReportLab not installed
        from django.contrib import messages
        messages.error(request, "ReportLab is not installed. Run 'pip install reportlab' to enable PDF generation.")
        from django.http import HttpResponseRedirect
        return HttpResponseRedirect(request.get_full_path())

class AstrologyAdminSite(admin.AdminSite):
    site_header = "Prarabdha Jyotish Kendra | Business Intelligence"
    site_title = "Admin Dashboard"
    index_title = "Astrology Analytics & Operations"
    index_template = "admin/index.html"

    def index(self, request, extra_context=None):
        from datetime import timedelta
        now = timezone.now()
        
        # Date boundaries
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        year_ago = now - timedelta(days=365)
        
        # Today
        today_p = PalmReading.objects.filter(created_at__date=now.date()).count()
        today_k = Kundali.objects.filter(created_at__date=now.date()).count()
        
        # Week
        week_p = PalmReading.objects.filter(created_at__gte=week_ago).count()
        week_k = Kundali.objects.filter(created_at__gte=week_ago).count()
        
        # Month
        month_p = PalmReading.objects.filter(created_at__gte=month_ago).count()
        month_k = Kundali.objects.filter(created_at__gte=month_ago).count()
        
        # Year
        year_p = PalmReading.objects.filter(created_at__gte=year_ago).count()
        year_k = Kundali.objects.filter(created_at__gte=year_ago).count()
        
        # Total
        total_p = PalmReading.objects.count()
        total_k = Kundali.objects.count()
        
        # Revenue Calculation Variables
        P_PRICE = 251
        K_PRICE = 751
        
        today_income = (today_p * P_PRICE) + (today_k * K_PRICE)
        week_income = (week_p * P_PRICE) + (week_k * K_PRICE)
        month_income = (month_p * P_PRICE) + (month_k * K_PRICE)
        year_income = (year_p * P_PRICE) + (year_k * K_PRICE)
        total_income = (total_p * P_PRICE) + (total_k * K_PRICE)

        extra_context = extra_context or {}
        extra_context.update({
            # Overview
            'today_income': today_income,
            'total_income': total_income,
            'total_p': total_p,
            'total_k': total_k,
            
            # Modal Detailed Breakdowns
            'today_p_income': today_p * P_PRICE,
            'today_k_income': today_k * K_PRICE,
            'today_p_count': today_p,
            'today_k_count': today_k,
            
            # Chart Data (JSON representation for Chart.js)
            'chart_data_labels': ['Today', 'Last 7 Days', 'Last 30 Days', 'Last Year', 'All Time'],
            'chart_data_palm': [today_p * P_PRICE, week_p * P_PRICE, month_p * P_PRICE, year_p * P_PRICE, total_p * P_PRICE],
            'chart_data_kundali': [today_k * K_PRICE, week_k * K_PRICE, month_k * K_PRICE, year_k * K_PRICE, total_k * K_PRICE],
        })
        
        return super().index(request, extra_context)

custom_admin_site = AstrologyAdminSite(name='custom_admin')

@admin.register(PalmReading, site=custom_admin_site)
class PalmReadingAdmin(admin.ModelAdmin):
    list_display = ('hand_image_preview', 'name', 'phone', 'amount', 'status', 'created_at')
    list_editable = ('status',)
    list_display_links = ('name',)
    readonly_fields = ('preview_large',)
    search_fields = ('name', 'phone')
    actions = [generate_pdf_report]

    def amount(self, obj): 
        return "₹251"
    amount.short_description = "Revenue"

    def hand_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 5px; border: 1px solid #D4AF37;"/>'
                '</a>', 
                obj.image.url, obj.image.url
            )
        return format_html('<span style="color: #888;">No Image</span>')
    hand_image_preview.short_description = "Hand"

    def preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 500px; border-radius: 15px; border: 3px solid #D4AF37;"/>', obj.image.url)
        return "No Image"
    preview_large.short_description = "Full Image"

@admin.register(Kundali, site=custom_admin_site)
class KundaliAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'dob', 'birth_time', 'amount', 'status', 'created_at')
    list_editable = ('status',)
    search_fields = ('name', 'phone')
    actions = [generate_pdf_report]
    
    def amount(self, obj): 
        return "₹751"
    amount.short_description = "Revenue"