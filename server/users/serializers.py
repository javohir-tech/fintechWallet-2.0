# ================== REST FRAMEWORK ===============
from rest_framework import serializers

# ================= MODELS =====================
from users.models import User, AuthType

# ================= SHARED =================\
from shared.utilits import check_user_input


class SignUpSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email_or_number"] = serializers.CharField(
            max_length=64, write_only=True
        )

    class Meta:
        model = User
        fields = ["id", "auth_type", "auth_status"]
        extra_kwargs = {
            "id": {"read_only": True},
            "auth_type": {"read_only": True},
            "auth_status": {"read_only": True},
        }

    def validate(self, data):
        super().validate(data)
        data = self.check_auth_type(data)
        data = self.check_exists(data)
        
        return data

    @staticmethod
    def check_auth_type(data):
        user_input = data["email_or_number"]
        if check_user_input(user_input) == AuthType.VIA_EMAIL:
            data = {"email": user_input, "auth_type": AuthType.VIA_EMAIL}
        elif check_user_input(user_input) == AuthType.VIA_PHONE:
            data = {"phone_number": user_input, "auth_type": AuthType.VIA_PHONE}
        else:
            raise serializers.ValidationError("email or phone number is not valid")

        return data

    @staticmethod
    def check_exists(data):
        auth_type = data["auth_type"]

        if auth_type == AuthType.VIA_EMAIL:
            email = data.get("email", None)
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("This email already is exist")
        elif auth_type == AuthType.VIA_PHONE:
            phone_number = data.get("phone_number")
            if User.objects.filter(phone_number=phone_number).exists():
                raise serializers.ValidationError("This phone number already exist")

        return data

    def create(self, validated_data):
        user: User = User(**validated_data)
        user.save()

        