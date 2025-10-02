from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from collects.models import Collection
from payments.models import Payment

# @shared_task(
#     retry_kwargs={"max_retries": 5, "countdown": 60},
#     retry_backoff=True,
#     retry_jitter=True,
# )


@shared_task
def send_collection_created_email(collect_id):
    """Отправить письмо автору о создании сбора"""
    print('Письмо отправлено!')
    request = Collection.objects.get(id=collect_id)
    subject = "Ваш сбор успешно создан!"
    message = (
        f"Здравствуйте!\n\n"
        f"Ваш сбор «{request.name}» (ID: {collect_id}) успешно создан.\n"
        f"Теперь вы можете принимать платежи.\n\n"
        "С уважением, команда Donution"
    )
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.author.email],
    )
    email.send()


@shared_task
def send_payment_created_email(payment_id):
    """Отправить письмо автору сбора о новом платеже"""
    print('Письмо отправлено!')

    request = Payment.objects.get(id=payment_id)
    subject = "Ваш платеж успешно создан!"
    message = (
        f"Здравствуйте!\n\n"
        f"Ваш платеж для сбора «{request.collect.title}»"
        f"на сумму  {request.amount}. Успешно создан\n\n"
        "С уважением, команда Donution."
    )
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[request.author.email],
    )
    email.send()
