from django.apps import AppConfig
from threading import Thread


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'
    
    
    def ready(self):
        from .consumers.student_events import start_consumer
        # Lancer le consumer dans un thread pour ne pas bloquer le démarrage de Django
        Thread(target=start_consumer, daemon=True).start()
