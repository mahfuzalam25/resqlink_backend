from django.core.mail import send_mail

def send_otp_email(email, otp, purpose="Password Reset"):
    subject = f"{purpose} Verification Code"
    message = f"Your verification code is: {otp}. It will expire in 10 minutes."
    from_email = "crack404websol@gmail.com"
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
