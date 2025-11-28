from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage, FAQ, Testimonial, SiteSettings, TeamMember, SiteStatistics

def index(request):
    """Home page view"""
    site_settings = SiteSettings.get_settings()
    statistics = SiteStatistics.get_stats()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    faqs = FAQ.objects.filter(is_active=True)[:6]
    
    context = {
        'site_settings': site_settings,
        'statistics': statistics,
        'testimonials': testimonials,
        'faqs': faqs,
    }
    return render(request, 'pages/index.html', context)


def about(request):
    """About page view"""
    site_settings = SiteSettings.get_settings()
    team_members = TeamMember.objects.filter(is_active=True).select_related('user')
    statistics = SiteStatistics.get_stats()
    
    context = {
        'site_settings': site_settings,
        'team_members': team_members,
        'statistics': statistics,
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    """Contact page view"""
    site_settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        if not name or not email or not subject or not message_text:
            messages.error(request, 'جميع الحقول مطلوبة!')
            return redirect('pages:contact')
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message_text
        )
        
        messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.')
        return redirect('pages:contact')
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'pages/contact.html', context)