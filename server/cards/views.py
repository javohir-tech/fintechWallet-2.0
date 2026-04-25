from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CardLookupSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CardLookupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CardLookupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.get_result())


# Create your views here.
