from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import ContactSerializer
from .models import ContactMessage
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class ContactAdminAPI(APIView):
    def post(self, request, format=None):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your message has been sent to the admin. Thank you!'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactDetailsAPI(APIView):
    def get(self, request, format=None):
        messages = ContactMessage.objects.all()
        serializer = ContactSerializer(messages, many=True)
        return Response(serializer.data)