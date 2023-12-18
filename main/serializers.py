from rest_framework import serializers

class AdmissionSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30)
    age = serializers.IntegerField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField(max_length=12)
    gender = serializers.CharField(max_length=10)
    batch_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    payment_successful = serializers.BooleanField()


class AdmissionUpdateSerializer(serializers.Serializer):
    email=serializers.EmailField()
    batch_id=serializers.IntegerField()
    payment_successful=serializers.BooleanField()
    amount = serializers.IntegerField()

