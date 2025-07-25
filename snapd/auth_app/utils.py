
import random
import string
from datetime import timedelta


expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = OTP.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)