from django.urls import path
from .views import UploadCsvView, UploadPdfView, UploadImageView

urlpatterns = [
    path('upload/csv/', UploadCsvView.as_view(), name='upload-csv'),
    path('upload/pdf/', UploadPdfView.as_view(), name='upload-pdf'),
    path('upload/image/', UploadImageView.as_view(), name='upload-image'),
]
