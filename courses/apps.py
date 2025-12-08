from django.apps import AppConfig
from threading import Thread
from .consumers.student_events import start_consumer

class CourseConfig(AppConfig):
    name = 'course'

    def ready(self):
        Thread(target=start_consumer).start()