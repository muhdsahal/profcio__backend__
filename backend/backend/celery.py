from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE','backend.settings')
app = Celery('backend')
app.conf.enable_utc = False


app.conf.update(timezone ='Asia/Mumbai')

app.config_from_object(settings,namespace='CELERY')

#Celery Beat Settings

app.conf.beat_schedule = {
  'send-booking-reminders': {
    'task': 'employee.tasks.send_booking_reminders',
    'schedule': crontab(hour=20, minute=40),  # Set the schedule as needed
    },
}



app.autodiscover_tasks()
@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')


  # 'send-mail-every-day-at-8':{
    #     'task':'employee.tasks.celerybeatcheck',
    #     'schedule':crontab(hour=0,minute=5),
    #     # 'schedule':crontab(),
    #     # 'args':(2,)
    # },