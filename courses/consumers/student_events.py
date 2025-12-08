import pika, json
from django.conf import settings
from ..models import StudentCourse, Course

def start_consumer():
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
        student_id = data["student_id"]
        course_id = data["course_id"]

        course = Course.objects.get(id=course_id)
        StudentCourse.objects.get_or_create(
            student_id=student_id,
            course=course
        )

        print("✔️ Association student-course traitée via RabbitMQ")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print("🎧 Listening for student events...")
    channel.start_consuming()