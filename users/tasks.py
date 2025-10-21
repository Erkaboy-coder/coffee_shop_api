from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import User
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def delete_unverified_users():
    # Delete users who are not verified within 2 days
    cutoff = timezone.now() - timedelta(days=2)
    qs = User.objects.filter(is_verified=False, date_joined__lt=cutoff)
    count = qs.count()
    qs.delete()
    return f"{count} unverified users deleted"


@shared_task
def send_verification_email(email, code):
    """Send email verification code asynchronously."""
    subject = "Your Coffee Shop Verification Code"
    message = (
        f"Hello!\n\n"
        f"Your verification code is: {code}\n"
        f"This code will expire in 1 hour.\n\n"
        f"Thanks,\nCoffee Shop Team ☕"
    )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        print(f"[EMAIL SENT] Verification code {code} sent to {email}")
    except Exception as e:
        print(f"[EMAIL ERROR] Failed to send code to {email}: {e}")