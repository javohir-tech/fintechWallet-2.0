# ================== REST FRAMEWORK ===============
from rest_framework import serializers

# ================= MODELS =====================
from users.models import User

class SignUpSerializer(serializers.ModelSerializer):
    
    class  Meta:
        model = User