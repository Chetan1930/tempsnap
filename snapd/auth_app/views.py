from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .utils import generate_code,is_expired

from .models import OTP, ParticipantVerification


class RequestOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        email = request.data.get('email')

        if not phone and not email:
            raise ValidationError("Phone number is required.")

        # Create or get the user
        user = ParticipantVerification.objects.filter(phone=phone, email=email).first()
        if not user:
            user = ParticipantVerification.objects.create(
                phone=phone,
                email=email,
                is_verified=False
            )


        # Create a new OTP instance
        match_otp = generate_code()
        
        OTP.objects.create(
            user=user,
            code=match_otp,
        )

        return Response({
            "message": "OTP sent successfully",
            "phone": phone,
            "OTP": match_otp,
        })

    def get(self, request):
        return Response({"message": "Use POST to request an OTP"})


class VerifyOTPView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        email = request.data.get('email')
        code_ = request.data.get('code')

        if not (phone or email):
            raise ValidationError("Phone or email is required.")

        if not code_:
            raise ValidationError("OTP is required.")

        # Get the user
        user,_ = ParticipantVerification.objects.get_or_create(phone=phone, email=email)
        
        # Get the latest OTP for this user
        otp = OTP.objects.filter(user=user).order_by('-created_at').first()
        if not otp:
            raise ValidationError("No OTP found for this user.")

        # Check if OTP matches
        if otp.code != code_:
            raise ValidationError("Incorrect OTP.")

        # Check expiry
        if otp.is_expired():
            raise ValidationError("OTP has expired.")

        # Optionally mark the user as verified
        # user.is_verified = True
        # user.save()

        # Optionally delete used OTP
        # otp.delete()

        # Issue tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "message": "OTP verified successfully",
        })
