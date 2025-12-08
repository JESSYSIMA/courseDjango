import pika
import json

def start_consumer():
    # Importer les modèles à l'intérieur de la fonction pour éviter AppRegistryNotReady
    from ..models import StudentCourse, Course

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost')
    )
    channel = connection.channel()

    channel.exchange_declare(exchange='student-events', exchange_type='topic')

    queue = channel.queue_declare(queue='', exclusive=True)
    queue_name = queue.method.queue

    channel.queue_bind(
        exchange='student-events',
        queue=queue_name,
        routing_key='student.course.associate'
    )

    def callback(ch, method, properties, body):
        data = json.loads(body)
        student_id = data.get("student_id")
        course_id = data.get("course_id")

        try:
            course = Course.objects.get(id=course_id)
            StudentCourse.objects.get_or_create(
                student_id=student_id,
                course=course
            )
            print(f"✔️ Association student-course traitée pour student_id={student_id}, course_id={course_id}")
        except Course.DoesNotExist:
            print(f"❌ Course avec id={course_id} introuvable")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("🎧 Listening for student events...")
    channel.start_consuming()
