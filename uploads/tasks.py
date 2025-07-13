from celery import shared_task
from .models import ETLJob
from django.utils import timezone
import time

@shared_task
def process_etl_job(etl_job_id):
    try:
        etl_job = ETLJob.objects.get(id=etl_job_id)
        etl_job.status = 'processing'
        etl_job.started_at = timezone.now()
        etl_job.save()
        time.sleep(40)
        # TODO: perform your ETL steps here
        # e.g., read file, validate, transform, save results

        etl_job.status = 'completed'
        etl_job.completed_at = timezone.now()
        etl_job.save()
    except Exception as e:
        etl_job.status = 'failed'
        etl_job.error_message = str(e)
        etl_job.completed_at = timezone.now()
        etl_job.save()
