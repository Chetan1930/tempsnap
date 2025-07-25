import uuid
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField  
from django.utils import timezone
from datetime import timedelta

# --- Abstract Timestamp Mixin ---
class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --- User Model ---
class ParticipantVerification(TimeStamps):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["phone", "email"], name="unique_phone_email")
        ]


    def __str__(self):
        return self.phone.as_e164 if self.phone else (self.email or "User")

# --- OTP Model ---
class OTP(TimeStamps):
    code = models.CharField(max_length=6)
    expires_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        ParticipantVerification,
        on_delete=models.CASCADE,
        related_name="otps"
    )
    
    def is_expired(self):
        print(timezone.now(), self.expires_at+ timedelta(minutes=5))
        return timezone.now() > self.expires_at + timedelta(minutes=5)

    def __str__(self):
        return f"OTP for {self.user} - {self.code}"
