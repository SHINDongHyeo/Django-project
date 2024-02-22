from celery import shared_task
from django.db import transaction

import logging

logger = logging.getLogger(__name__)

@shared_task()
def celery_check():
    with open("test.txt", "a")  as f:
        f.write("확인")
    print("확인용ㅇㅇㄹㄴㅇㄹㄴㅇㄹㅇㄴㄹㅇㄴㄹ")
    logger.info("Starting to update congestion data.")
    