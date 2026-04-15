# ================== REST FRAMEWORK ===============
from rest_framework import serializers

# ================= MODELS =====================
from users.models import User, AuthType, UserConfirmation , AuthStatus

# ================= SHARED =================
from shared.utilits import check_user_input, send_email, check_password

# ================ TOKEN ===================
from .tokens import RegistrationToken


class SignUpSerializer(serializers.ModelSerializer):
    """SIGNUP SERIALIZER"""

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

        auth_type = validated_data.get("auth_type")
        if auth_type == AuthType.VIA_EMAIL:
            email = validated_data.get("email")
            code = user.create_code(auth_type)
            send_email(email, code)
        elif auth_type == AuthType.VIA_PHONE:
            phone_number = validated_data.get("phone_number")
            code = user.create_code(auth_type)
            send_email(phone_number, code)

        return user

    def to_representation(self, instance: User):
        data = super().to_representation(instance)
        token = RegistrationToken.for_user(instance)
        data["verify_token"] = str(token)
        return data


class VerifyCodeSerializer(serializers.Serializer):
    """Tastiqlsh kodi"""

    code = serializers.CharField(max_length=4, min_length=4)

    def validate_code(self, value: str):

        if not value.isdigit():
            raise serializers.ValidationError("code is not valid")

        return value


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password", "auth_status"]
        read_only_fields = ["id", "auth_status"]

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("this username is already exist")

        return value

    def validate_password(self, value):

        check_password(value)

        return value
    
    def update(self, instance:User, validated_data):
        
        for item , value in validated_data.items():
            setattr(instance, item , value)
        
        instance.auth_status =  AuthStatus.DONE
        instance.save()
        return instance
    
    def to_representation(self, instance:User):
        data =  super().to_representation(instance)
        data.update(instance.token())
        return data