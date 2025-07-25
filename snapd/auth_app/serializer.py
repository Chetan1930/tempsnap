from rest_framework import serializers
from .models import ParticipantVerification, OTP

class ParticipantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParticipantVerification
        fields = '__all__'


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'
