from django.core.mail import EmailMessage, get_connection

from .models import SiteSettings


def get_site_settings():
    return SiteSettings.objects.first() or SiteSettings()


def build_email_connection(site=None):
    site = site or get_site_settings()
    if site.smtp_host and site.smtp_username and site.smtp_password:
        return get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=site.smtp_host,
            port=site.smtp_port or 587,
            username=site.smtp_username,
            password=site.smtp_password,
            use_tls=site.smtp_use_tls,
        )

    return get_connection('django.core.mail.backends.console.EmailBackend')


def send_site_email(subject, body, recipients, site=None, reply_to=None):
    site = site or get_site_settings()
    from_email = site.smtp_from_email or site.email or 'noreply@localhost'
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=from_email,
        to=recipients,
        connection=build_email_connection(site),
        reply_to=reply_to or [],
    )
    email.send(fail_silently=False)