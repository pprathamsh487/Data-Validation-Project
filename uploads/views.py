# uploads/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import CsvUploadSerializer, PdfUploadSerializer, ImageUploadSerializer

class UploadCsvView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CsvUploadSerializer(data=request.data)
        if serializer.is_valid():
            # Optionally: check file extension
            file = request.FILES.get('file')
            if not file.name.endswith('.csv'):
                return Response({'error': 'Only CSV files allowed.'}, status=400)
            serializer.save(user=request.user, status='pending')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UploadPdfView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PdfUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get('file')
            if not file.name.endswith('.pdf'):
                return Response({'error': 'Only PDF files allowed.'}, status=400)
            serializer.save(user=request.user, status='pending')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get('file')
            if not (file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.jpeg')):
                return Response({'error': 'Only image files allowed.'}, status=400)
            serializer.save(user=request.user, status='pending')
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
