# uploads/serializers.py
from rest_framework import serializers
from .models import Upload

class BaseUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['id', 'file', 'file_type', 'uploaded_at', 'status']
        read_only_fields = ['id', 'uploaded_at', 'status', 'file_type']  # file_type will be set in view

class CsvUploadSerializer(BaseUploadSerializer):
    def create(self, validated_data):
        validated_data['file_type'] = 'csv'
        return super().create(validated_data)

class PdfUploadSerializer(BaseUploadSerializer):
    def create(self, validated_data):
        validated_data['file_type'] = 'pdf'
        return super().create(validated_data)

class ImageUploadSerializer(BaseUploadSerializer):
    def create(self, validated_data):
        validated_data['file_type'] = 'image'
        return super().create(validated_data)