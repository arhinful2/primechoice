from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# ---------- SITE SETTINGS (single instance) ----------
class SiteSettings(models.Model):
    school_name = models.CharField(max_length=200, default="Prime Choice Kids Care", blank=True)
    tagline = models.CharField(max_length=300, default="Join us and be part of shaping young minds!", blank=True)
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_title = models.CharField(max_length=200, default='Welcome to Prime Choice Kids Care', blank=True)
    hero_text = RichTextField(blank=True, default='')
    about_title = models.CharField(max_length=200, default='About Us', blank=True)
    about_us = RichTextField(blank=True, default='')
    mission_title = models.CharField(max_length=200, default='Mission', blank=True)
    mission_text = RichTextField(blank=True, default='')
    vision_title = models.CharField(max_length=200, default='Vision', blank=True)
    vision_text = RichTextField(blank=True, default='')
    why_choose_us = RichTextField(blank=True, default='', help_text='Describe why parents should choose the school')
    admissions_title = models.CharField(max_length=200, default='Admissions', blank=True)
    admissions_overview = RichTextField(blank=True, default='')
    admissions_requirements = RichTextField(blank=True, default='')
    contact_title = models.CharField(max_length=200, default='Contact Us', blank=True)
    contact_intro = RichTextField(blank=True, default='')
    phone1 = models.CharField(max_length=20, default='0541961061', blank=True)
    phone2 = models.CharField(max_length=20, default='0244303267', blank=True)
    whatsapp_phone = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(default='info@primechoicekids.com', blank=True)
    notification_email = models.EmailField(blank=True, default='')
    location = models.CharField(max_length=500, default='New Baakoyeden', blank=True)
    opening_hours = models.CharField(max_length=200, blank=True, default='')
    map_embed_code = models.TextField(blank=True, default='')
    footer_text = models.TextField(blank=True, default='')
    facebook = models.URLField(blank=True, default='')
    instagram = models.URLField(blank=True, default='')
    youtube = models.URLField(blank=True, default='')
    tiktok = models.URLField(blank=True, default='')
    linkedin = models.URLField(blank=True, default='')
    twitter = models.URLField(blank=True, default='')
    pinterest = models.URLField(blank=True, default='')
    whatsapp_url = models.URLField(blank=True, default='', help_text='WhatsApp business profile or group URL')
    smtp_host = models.CharField(max_length=255, blank=True, default='')
    smtp_port = models.PositiveIntegerField(blank=True, null=True)
    smtp_use_tls = models.BooleanField(default=True)
    smtp_username = models.CharField(max_length=255, blank=True, default='')
    smtp_password = models.CharField(max_length=255, blank=True, default='')
    smtp_from_email = models.EmailField(blank=True, default='')
    
    # Database Configuration (for Vercel/production deployment)
    db_engine = models.CharField(max_length=20, default='sqlite3', blank=True, choices=[('sqlite3', 'SQLite3'), ('postgresql', 'PostgreSQL')], help_text='Database engine to use')
    db_host = models.CharField(max_length=255, blank=True, default='', help_text='Database host (e.g., localhost or Vercel-provided host)')
    db_port = models.CharField(max_length=10, blank=True, default='', help_text='Database port (e.g., 5432 for PostgreSQL)')
    db_name = models.CharField(max_length=255, blank=True, default='', help_text='Database name')
    db_user = models.CharField(max_length=255, blank=True, default='', help_text='Database username')
    db_password = models.CharField(max_length=255, blank=True, default='', help_text='Database password')
    
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # force single instance
        super().save(*args, **kwargs)

    def __str__(self):
        return "Site Settings"


# ---------- HOMEPAGE MEDIA AND SOCIAL PROOF ----------
class StaffMember(models.Model):
    name = models.CharField(max_length=120, blank=True, default='')
    role = models.CharField(max_length=120, blank=True, default='', help_text='Job title or position (e.g., Principal, Teacher, Caregiver)')
    bio = models.TextField(blank=True, default='', help_text='Short biography or description')
    photo = models.ImageField(upload_to='staff/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name or 'Staff member'


class Testimonial(models.Model):
    name = models.CharField(max_length=120, blank=True, default='')
    role = models.CharField(max_length=120, blank=True, default='')
    quote = models.TextField(blank=True, default='')
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.name or 'Testimonial'


class GalleryImage(models.Model):
    title = models.CharField(max_length=150, blank=True, default='')
    image = models.ImageField(upload_to='gallery/', blank=True, null=True)
    caption = models.CharField(max_length=255, blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title or 'Gallery image'


class StatCounter(models.Model):
    label = models.CharField(max_length=120, blank=True, default='')
    value = models.PositiveIntegerField(default=0)
    suffix = models.CharField(max_length=20, blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.label or 'Stat counter'


class NewsEvent(models.Model):
    title = models.CharField(max_length=180, blank=True, default='')
    slug = models.SlugField(max_length=220, unique=True, blank=True, default='')
    summary = models.TextField(blank=True, default='')
    date = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=180, blank=True, default='')
    cta_text = models.CharField(max_length=60, blank=True, default='')
    cta_url = models.URLField(blank=True, default='')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-date', '-created_at']

    def __str__(self):
        return self.title or 'News and event'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_title = self.title or 'news-event'
            base_slug = slugify(base_title)[:200] or 'news-event'
            slug = base_slug
            counter = 2
            while NewsEvent.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ClickMetric(models.Model):
    ACTION_CHOICES = [
        ('call', 'Call'),
        ('whatsapp', 'WhatsApp'),
        ('cta', 'CTA'),
        ('social', 'Social'),
        ('nav', 'Navigation'),
    ]

    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, default='cta')
    label = models.CharField(max_length=120, blank=True, default='')
    target_url = models.CharField(max_length=500, blank=True, default='')
    source_page = models.CharField(max_length=200, blank=True, default='')
    ip_address = models.CharField(max_length=64, blank=True, default='')
    user_agent = models.CharField(max_length=300, blank=True, default='')
    clicked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-clicked_at']

    def __str__(self):
        return f'{self.action_type} - {self.label or self.target_url}'

# ---------- PROGRAMS ----------
class Program(models.Model):
    PROGRAM_CHOICES = [
        ('creche', 'Crèche'),
        ('preschool', 'Preschool'),
        ('primary', 'Lower Primary'),
    ]
    program_type = models.CharField(max_length=20, choices=PROGRAM_CHOICES, unique=True)
    title = models.CharField(max_length=100, blank=True, default='')
    age_group = models.CharField(max_length=50, blank=True, default='')
    description = RichTextField(blank=True, default='')
    image = models.ImageField(upload_to='programs/', blank=True, null=True)
    order = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']

# ---------- VACANCIES / CAREERS ----------
class Vacancy(models.Model):
    title = models.CharField(max_length=200, blank=True, default='')
    qualifications = RichTextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    posted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ---------- CONTACT MESSAGES ----------
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    replied = models.BooleanField(default=False)
    reply_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"