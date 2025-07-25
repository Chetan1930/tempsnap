from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User


from .models import OTP, ParticipantVerification


class RequestOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        
        print(phone)

        if not phone:
            raise ValidationError("Phone number is required.")

        # Create or get the user
        # user, _ = ParticipantVerification.objects.get_or_create(
        #     phone=phone,
        #     defaults={"is_verified": False}
        # )

        # # Create a new OTP instance
        # otp = OTP.objects.create(user=user)

        # # 🔔 Simulate sending OTP (log to console for now)
        # print(f"[DEBUG] OTP for {phone}: {otp.code}")

        return Response({
            "message": "OTP sent successfully",
            "phone": phone,
            # "otp": otp.code  # ⚠️ Show only in development
        })

    def get(self, request):
        return Response({"message": "Use POST to request an OTP"})


class VerifyOTPView(APIView):
    def post(self, request):
        # phone = request.data.get('phone')
        code = request.data.get('otp')

        if not phone or not code:
            raise ValidationError("Phone and OTP are required.")

        # user = ParticipantVerification.objects.get(phone=phone)
        # try:
        # except ParticipantVerification.DoesNotExist:
        #     raise ValidationError("User does not exist.")

        # otp = OTP.objects.filter(user=user, code=code).order_by('-created_at').first()

        if not otp or otp.is_expired():
            raise ValidationError("Invalid or expired OTP.")

        # otp.delete()  # Optional cleanup

        # Generate JWT
        refresh = RefreshToken.for_user(User)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })
