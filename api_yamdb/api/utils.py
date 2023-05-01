import random

from django.core.mail import send_mail


def generate_confirmation_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_email_with_verification_code(user):
    user.confirmation_code = generate_confirmation_code()
    user.save()
    email = user.email
    username = user.username
    confirmation_code = user.confirmation_code
    send_mail(
        subject='Письмо подтверждения',
        from_email='yamdb@expressdelivery.com',
        recipient_list=[email, ],
        message=(f'Привет, {username}! '
                 'Это письмо содержит код подтверждения. Вот он:\n'
                 f'<b>{confirmation_code}</b>.\n'
                 'Чтоб получить токен, отправьте запрос\n'
                 'с полями username и confirmation_code'
                 'на /api/v1/auth/token/.'),
    )
