# portal/tasks.py
from celery import shared_task
from datetime import datetime
from . models import Time, TestStatus, TestHour
from datetime import datetime, timedelta
import pytz

@shared_task
def print_hello():
    current_time = datetime.now(pytz.utc)
    times = Time.objects.all() # fetching

    for time in times:
        user_start_time = time.start_time
        time_difference = current_time-user_start_time

        test_hours = TestHour.objects.filter(test=time.test).first()

        if(time_difference >= timedelta(hours=test_hours.time.hour, minutes=test_hours.time.minute, seconds=test_hours.time.second)):
            test_status = TestStatus.objects.filter(user=time.user, test=time.test).first()
            if(test_status is None):
                return
            test_status.test_status = '2'
            test_status.save()
