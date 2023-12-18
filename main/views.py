from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .services import AdmissionService
from .serializers import AdmissionSerializer, AdmissionUpdateSerializer
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

class AdmissionViewSet(viewsets.ViewSet):

    def enroll_student(self, request):
        serializer = AdmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        admission_service = AdmissionService()
        status, msg = admission_service.register(serializer.validated_data)

        if not status:
            return Response({'error': msg}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': msg}, status=HTTP_200_OK)

    def update_student(self, request):
        serializer = AdmissionUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        admission_service = AdmissionService()
        status, msg = admission_service.update_form(serializer.validated_data)

        if not status:
            return Response({'error': msg}, status=HTTP_400_BAD_REQUEST)
        
        return Response({'message': msg}, status=HTTP_200_OK)
    

    
        
