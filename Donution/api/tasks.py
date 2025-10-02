from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import now

from collects.models import Collection
from payments.models import Payment


@shared_task
def send_collection_created_email(collect_id):
    """Отправить письмо автору о создании сбора"""
    collection = Collection.objects.get(id=collect_id)
    subject = "Your collection created"
    message = (
        f"Dear, {collection.author.first_name}!\n\n"
        f"Your collection '{collection.title}' has been successfully "
        "created.\n"
        'Below is the link to participate in this collection:\n'
        # добавить ссылку на платежный эндпоинт\\\\n\\\\n"
        "Sincerely, Donution team"
    )

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[collection.author.email],
    )
    email.send(fail_silently=False)


@shared_task
def send_payment_created_email(payment_id):
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


@shared_task(name='old_collection_task')
def old_collection_task():
    current_time = now()
    collections_to_unactivate = Collection.objects.filter(
        end_time_lte=current_time)
    collections_to_unactivate.bulk_update(is_active=False)
    print(f'{collections_to_unactivate.count()} deactivated!')
