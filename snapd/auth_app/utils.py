import random
import string
from datetime import timedelta
from .models import OTP,ParticipantVerification
from django.utils import timezone




def is_expired():
    return timezone.now() > OTP.expires_at + timedelta(minutes=5)

def generate_code():
    return ''.join(random.choices(string.digits, k=6))
