from celery import shared_task
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone


def send_warranty_expiry_reminder(email, days_left):
    subject = 'Warranty Expiry Reminder'
    if days_left == 0:
        message = 'Your warranty has expired. Please contact us for renewal.'
    else:
        message = f'Your warranty will expire in {days_left} days.'
    sender_email = 'trivenimaurya@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)
