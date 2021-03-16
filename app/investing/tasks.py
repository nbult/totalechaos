import logging
from .models import Security
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def download_quotes():
    logger.info('Download Quotes...')

    for security in Security.objects.filter(scraper__isnull=False):
        security.download_quotes()
