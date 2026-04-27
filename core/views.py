import json

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import SiteSettings, Program, Vacancy, ContactMessage, Testimonial, GalleryImage, StatCounter, NewsEvent, StaffMember
from .models import ClickMetric
from .utils import get_site_settings, send_site_email

def common_context():
    site = get_site_settings()
    return {'site': site}

def home(request):
    site = get_site_settings()
    programs = Program.objects.all()[:3]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    gallery_images = GalleryImage.objects.filter(is_active=True)[:6]
    stats = StatCounter.objects.filter(is_active=True)[:4]
    latest_news = NewsEvent.objects.filter(is_active=True)[:3]
    featured_vacancy = Vacancy.objects.filter(is_active=True).first()
    context = {
        'programs': programs,
        'testimonials': testimonials,
        'gallery_images': gallery_images,
        'stats': stats,
        'latest_news': latest_news,
        'featured_vacancy': featured_vacancy,
        'site': site,
    }
    return render(request, 'core/home.html', context)

def about(request):
    staff_members = StaffMember.objects.filter(is_active=True)
    context = common_context()
    context['staff_members'] = staff_members
    return render(request, 'core/about.html', context)

def programs(request):
    programs = Program.objects.all()
    context = {'programs': programs}
    context.update(common_context())
    return render(request, 'core/programs.html', context)

def admissions(request):
    context = common_context()
    return render(request, 'core/admissions.html', context)

def careers(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    context = {'vacancies': vacancies}
    context.update(common_context())
    return render(request, 'core/careers.html', context)

def contact(request):
    site = get_site_settings()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message_text = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )

        # Send notification email to admin using admin-managed settings.
        admin_email = site.notification_email or site.email
        if admin_email:
            subject = f"New Contact Message from {name}"
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\n\nMessage:\n{message_text}"
            send_site_email(subject, body, [admin_email], site=site, reply_to=[email] if email else [])

        return render(request, 'core/contact_success.html', common_context())

    context = common_context()
    return render(request, 'core/contact.html', context)


def news_list(request):
    context = {
        'news_items': NewsEvent.objects.filter(is_active=True),
    }
    context.update(common_context())
    return render(request, 'core/news_list.html', context)


def news_detail(request, slug):
    item = get_object_or_404(NewsEvent, slug=slug, is_active=True)
    context = {
        'item': item,
        'related_news': NewsEvent.objects.filter(is_active=True).exclude(pk=item.pk)[:3],
    }
    context.update(common_context())
    return render(request, 'core/news_detail.html', context)


@csrf_exempt
@require_POST
def track_click(request):
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        payload = {}

    forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '')
    ip_address = forwarded_for.split(',')[0].strip() if forwarded_for else request.META.get('REMOTE_ADDR', '')
    user_agent = (request.META.get('HTTP_USER_AGENT') or '')[:300]

    ClickMetric.objects.create(
        action_type=(payload.get('action_type') or 'cta')[:20],
        label=(payload.get('label') or '')[:120],
        target_url=(payload.get('target_url') or '')[:500],
        source_page=(payload.get('source_page') or request.path)[:200],
        ip_address=ip_address[:64],
        user_agent=user_agent,
    )
    return JsonResponse({'ok': True})