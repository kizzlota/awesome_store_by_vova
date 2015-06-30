from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail.message import EmailMultiAlternatives
from binascii import hexlify
from os import urandom
from .models import RegistrationCode


def _generate_code():
    return hexlify(urandom(30))



def create_signup_code(user):
    code = _generate_code()
    user_code = RegistrationCode(code=code, username=user)
    user_code.save()
    return code



def send_email(user, prefix):
    subject_file = 'mail/%s_subject.txt' % prefix

    txt_file = 'mail/%s.txt' % prefix
    html_file = 'mail/%s.html' % prefix

    subject = render_to_string(subject_file).strip()
    from_email = settings.DEFAULT_EMAIL_FROM
    to = user.email
    bcc_email = settings.DEFAULT_EMAIL_BCC
    # Make some context available
    ctxt = {
        'email': user.email,
        'username': user.username,

        'code': create_signup_code(user)
    }
    text_content = render_to_string(txt_file, ctxt)
    html_content = render_to_string(html_file, ctxt)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to],
                                 bcc=[bcc_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
