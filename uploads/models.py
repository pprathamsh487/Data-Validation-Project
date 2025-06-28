from django.db import models

from django.conf import settings

class Upload(models.Model):
    FILE_TYPE_CHOICES = [
        ('csv', 'CSV File'),
        ('pdf', 'PDF Document'),
        ('image', 'Image File'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed
    
    class Meta:
        db_table = 'UPLOAD'
    def __str__(self):
        return f"{self.file_type} by {self.user.username} at {self.uploaded_at}"

class ETLJob(models.Model):
    upload = models.OneToOneField(Upload, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    summary = models.TextField(blank=True)  # e.g., '123 rows, 4 errors'
    
    class Meta:
        db_table = 'ETL_JOB'

class ValidationError(models.Model):
    etl_job = models.ForeignKey(ETLJob, on_delete=models.CASCADE)
    row_number = models.IntegerField(null=True, blank=True)
    column_name = models.CharField(max_length=255)
    error_message = models.TextField()
    
    class Meta:
        db_table = 'VALIDATION_ERROR'

