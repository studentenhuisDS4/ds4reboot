from django.conf import settings
from django.core.mail import send_mail

subject = 'Some subject'
from_email = settings.DEFAULT_FROM_EMAIL
message = 'This is my test message'
recipient_list = ['davidzwa@gmail.com']
html_message = '<h1>This is my HTML test</h1>'


send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)