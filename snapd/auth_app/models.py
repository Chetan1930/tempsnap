
import uuid


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField  # Assuming you're using this

# --- Abstract Timestamp Mixin ---
class TimeStamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# --- User Model ---
class ParticipantVerification(TimeStamps):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = PhoneNumberField(unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.phone.as_e164 if self.phone else (self.email or "User")

# --- OTP Model ---
class OTP(TimeStamps):
    code = models.CharField(max_length=6)
    user = models.ForeignKey(
        ParticipantVerification,
        on_delete=models.CASCADE,
        related_name="otps"
    )

    def __str__(self):
        return f"OTP for {self.user} - {self.code}"
