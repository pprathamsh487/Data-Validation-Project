from django.test import TestCase
from uploads.models import Upload, ETLJob
from users.models import CustomUser
from rest_framework.test import APIClient
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch
from uploads.tasks import process_etl_job

# Create your tests here.
class UploadTestCase(TestCase):
    def setUp(self):
        self.__user_data = {'username' : 'testuser',
                            'first_name' : 'test',
                            'last_name' : 'user',
                            'email' : 'testuser@gmail.com',
                            'password' : 'test@123'}
        self.__obj_users_1 = CustomUser.objects.create(**self.__user_data)
        self.__upload_data = {
                            'file': 'uploads/test_file',
                            'status' : 'pending',
                            'user_id' : self.__obj_users_1.id
                            }
        self.__obj_upload_1 = Upload.objects.create(**self.__upload_data)
    
    def test_upload_creation_obj(self):
        self.obj_count = Upload.objects.count()
        
        self.assertIn(self.__obj_upload_1.status,['pending', 'processing', 'completed'])
        self.assertEqual(self.obj_count, 1)
    def test_upload_creation_api(self):
        pass
        
class UploadViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser', password='test@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Prepare fake files
        self.pdf_file = SimpleUploadedFile(
            'test.pdf', b'%PDF-1.4 fake pdf content', content_type='application/pdf'
        )
        self.csv_file = SimpleUploadedFile(
            'test.csv', b'header1,header2\nvalue1,value2\n', content_type='text/csv'
        )
        self.image_file = SimpleUploadedFile(
            'test.png', b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00', content_type='image/png'
        )

    def object_creation_checks(self, response, file_type):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        upload = Upload.objects.get(file_type=file_type)
        self.assertEqual(upload.user, self.user)
        self.assertEqual(upload.file_type, file_type)
        self.assertIn(upload.status, ['pending', 'processing', 'completed'])

        etl_job = ETLJob.objects.get(upload=upload)
        self.assertEqual(etl_job.upload, upload)
        self.assertIn(etl_job.status, ['pending', 'processing', 'completed'])

    def test_upload_pdf_creates_upload_and_etljob(self):
        data = {'file': self.pdf_file, 'file_type': 'pdf', 'status': 'pending'}
        response = self.client.post(reverse('upload-pdf'), data, format='multipart')
        self.object_creation_checks(response, 'pdf')

    def test_upload_csv_creates_upload_and_etljob(self):
        data = {'file': self.csv_file, 'file_type': 'csv', 'status': 'pending'}
        response = self.client.post(reverse('upload-csv'), data, format='multipart')
        self.object_creation_checks(response, 'csv')

    def test_upload_image_creates_upload_and_etljob(self):
        data = {'file': self.image_file, 'file_type': 'image', 'status': 'pending'}
        response = self.client.post(reverse('upload-image'), data, format='multipart')
        self.object_creation_checks(response, 'image')
        
class ETLJobTestCase(TestCase):
    def setUp(self):
        self.__user_data = {'username' : 'testuser',
                            'first_name' : 'test',
                            'last_name' : 'user',
                            'email' : 'testuser@gmail.com',
                            'password' : 'test@123'}
        self.__obj_users_1 = CustomUser.objects.create(**self.__user_data)
        self.upload = Upload.objects.create(user =self.__obj_users_1, file='dummy.pdf')
        self.job = ETLJob.objects.create(upload = self.upload)
    def test_etl_job_defaults_to_pending(self): 
        self.assertEqual(self.job.status, 'pending')
        
    @patch('uploads.tasks.time.sleep', return_value=None)
    def test_process_etl_job_sets_status(self, _):
        process_etl_job(self.job.id)
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, 'completed')