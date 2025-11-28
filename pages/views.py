from django.shortcuts import render, redirect
from django.contrib import messages
from .models import (
    ContactMessage,
    FAQ,
    Offer,
    Testimonial,
    SiteStatistics,
    TeamMember,
)


def index(request):
    """Home page view"""
    statistics = SiteStatistics.get_stats()
    testimonials = Testimonial.objects.filter(is_active=True)[:6]
    offers = Offer.objects.filter(is_active=True)[:8]

    context = {
        "statistics": statistics,
        "testimonials": testimonials,
        "offers": offers,
    }
    return render(request, "pages/home-ar.html", context)


def about(request):
    """About page view"""
    team_members = TeamMember.objects.filter(is_active=True).select_related("user")
    statistics = SiteStatistics.get_stats()

    context = {
        "team_members": team_members,
        "statistics": statistics,
    }
    return render(request, "pages/about-ar.html", context)


def contact(request):
    """Contact page view"""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        if not name or not email or not subject or not message_text:
            messages.error(request, "جميع الحقول مطلوبة!")
            return redirect("pages:contact")

        ContactMessage.objects.create(
            name=name, email=email, subject=subject, message=message_text
        )

        messages.success(request, "تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.")
        return redirect("pages:contact")

    faqs = FAQ.objects.filter(is_active=True)

    context = {
        "faqs": faqs,
    }
    return render(request, "pages/contact-ar.html", context)
