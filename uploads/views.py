# uploads/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ETLJob
from .tasks import process_etl_job
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
            upload = serializer.save(user=request.user, status='pending')
            etl_job = ETLJob.objects.create(upload=upload, status='pending')
            # Trigger Celery task
            process_etl_job.delay(etl_job.id)
            
            return Response({
                'upload_id': upload.id,
                'etl_job_id': etl_job.id,
                'status': etl_job.status
            }, status=201)
            
        return Response(serializer.errors, status=400)

class UploadPdfView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PdfUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get('file')
            if not file.name.endswith('.pdf'):
                return Response({'error': 'Only PDF files allowed.'}, status=400)
            upload = serializer.save(user=request.user, status='pending')
            etl_job = ETLJob.objects.create(upload=upload, status='pending')
            # Trigger Celery task
            process_etl_job.delay(etl_job.id)
            
            return Response({
                'upload_id': upload.id,
                'etl_job_id': etl_job.id,
                'status': etl_job.status
            }, status=201)
        return Response(serializer.errors, status=400)

class UploadImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get('file')
            if not (file.name.endswith('.jpg') or file.name.endswith('.png') or file.name.endswith('.jpeg')):
                return Response({'error': 'Only image files allowed.'}, status=400)
            upload = serializer.save(user=request.user, status='pending')
            etl_job = ETLJob.objects.create(upload=upload, status='pending')
            # Trigger Celery task
            process_etl_job.delay(etl_job.id)
            
            return Response({
                'upload_id': upload.id,
                'etl_job_id': etl_job.id,
                'status': etl_job.status
            }, status=201)
        return Response(serializer.errors, status=400)
