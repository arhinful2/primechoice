from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import messages
from .models import SiteSettings, Program, Vacancy, ContactMessage, Testimonial, GalleryImage, StatCounter, NewsEvent, ClickMetric, StaffMember
from .utils import get_site_settings, send_site_email

# ---------- SITE SETTINGS ADMIN ----------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'email', 'location', 'updated_at')

    def has_add_permission(self, request):
        return False if SiteSettings.objects.exists() else True

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.objects.first()
        if obj:
            return redirect(reverse('admin:core_sitesettings_change', args=[obj.pk]))
        return super().changelist_view(request, extra_context)

    fieldsets = (
        ('Brand', {
            'fields': ('school_name', 'tagline', 'logo', 'favicon')
        }),
        ('Homepage', {
            'fields': ('hero_title', 'hero_text', 'hero_image')
        }),
        ('About', {
            'fields': ('about_title', 'about_us', 'mission_title', 'mission_text', 'vision_title', 'vision_text', 'why_choose_us')
        }),
        ('Admissions', {
            'fields': ('admissions_title', 'admissions_overview', 'admissions_requirements')
        }),
        ('Contact and Footer', {
            'fields': ('contact_title', 'contact_intro', 'phone1', 'phone2', 'whatsapp_phone', 'email', 'notification_email', 'location', 'opening_hours', 'map_embed_code', 'footer_text')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'youtube', 'tiktok', 'linkedin', 'twitter', 'pinterest', 'whatsapp_url')
        }),
        ('Email Setup', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_use_tls', 'smtp_username', 'smtp_password', 'smtp_from_email')
        }),
    )

# ---------- PROGRAM ADMIN ----------
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'program_type', 'age_group', 'featured', 'order')
    list_editable = ('featured', 'order')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name', 'role', 'bio')


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(StatCounter)
class StatCounterAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'suffix', 'is_active', 'order')
    list_editable = ('value', 'suffix', 'is_active', 'order')


@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'date', 'location', 'is_active', 'order')
    list_filter = ('is_active',)
    list_editable = ('is_active', 'order')
    search_fields = ('title', 'summary', 'location')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(ClickMetric)
class ClickMetricAdmin(admin.ModelAdmin):
    list_display = ('action_type', 'label', 'target_url', 'source_page', 'clicked_at')
    list_filter = ('action_type', 'clicked_at')
    search_fields = ('label', 'target_url', 'source_page')
    readonly_fields = ('action_type', 'label', 'target_url', 'source_page', 'ip_address', 'user_agent', 'clicked_at')

    def has_add_permission(self, request):
        return False

# ---------- VACANCY ADMIN ----------
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'posted_on')

# ---------- CONTACT MESSAGE ADMIN WITH REPLY FEATURE ----------
class ReplyForm(forms.Form):
    reply_message = forms.CharField(widget=forms.Textarea, label="Your Reply")

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'sent_at', 'replied')
    list_filter = ('replied',)
    readonly_fields = ('name', 'email', 'phone', 'message', 'sent_at', 'replied', 'reply_text')
    search_fields = ('name', 'email')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:message_id>/reply/', self.admin_site.admin_view(self.reply_view), name='contactmessage-reply'),
        ]
        return custom_urls + urls

    def reply_view(self, request, message_id):
        message = get_object_or_404(ContactMessage, pk=message_id)
        site = get_site_settings()
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            if form.is_valid():
                reply_text = form.cleaned_data['reply_message']
                # Send email to the person
                subject = f"Reply from {site.school_name}"
                body = f"Dear {message.name},\n\n{reply_text}\n\nBest regards,\n{site.school_name}"
                send_site_email(subject, body, [message.email], site=site)
                # Save reply info
                message.reply_text = reply_text
                message.replied = True
                message.save()
                self.message_user(request, "Reply sent and saved!", level=messages.SUCCESS)
                return redirect(reverse('admin:core_contactmessage_changelist'))
        else:
            form = ReplyForm()
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            message=message,
            title="Reply to Contact Message",
        )
        return render(request, 'admin/core/contactmessage/reply.html', context)