from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.timezone import now

from collects.models import Collection
from Donution.celery_app import app
from payments.models import Payment


@shared_task
def send_collection_created_email(collect_id: int) -> str:
    """Отправить письмо автору о создании сбора"""
    collection = Collection.objects.get(id=collect_id)
    subject = "Your collection created"
    url = reverse('api_v1:collections-payments', args=(collect_id,))
    link = f'{settings.HOST_URL}{url}'
    message = (
        f"Dear, {collection.author.first_name}!\n\n"
        f"Your collection '{collection.title}' has been successfully "
        "created.\n"
        'Below is the link to participate in this collection:\n'
        f'{link}\n\n'
        "Sincerely, Donution team"
    )

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[collection.author.email],
    )
    email.send(fail_silently=False)
    return f'E-mail to author sended! {link}'


@shared_task
def send_payment_created_email(payment_id: int) -> str:
    """Send confirmation mail to payer."""

    payment = Payment.objects.get(id=payment_id)
    subject = "Your payment created!"
    message = (
        f"Dear, {payment.payer.first_name}!\n\n"
        f"Your payment for the collection '{payment.collect.title}'"
        f"in the amount of {payment.amount} has been successfully created.\n\n"
        "Sincerely, Donution team."
    )

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[payment.payer.email],
    )
    email.send()
    return 'E-mail to payer sended!'


@app.task
def old_collection_task() -> str:
    """Deactivate expired collections."""
    current_time = now()
    collections_to_unactivate = Collection.objects.filter(
        end_time__lte=current_time, is_active=True
        )
    for collection in collections_to_unactivate:
        collection.is_active = False
        collection.save()
    return f'{collections_to_unactivate.count()} collections deactivated!'
