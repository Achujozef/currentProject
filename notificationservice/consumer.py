import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "notificationservice.settings")
django.setup()

from api.models import *

params = pika.URLParameters('amqps://gllbrcms:rjjATZz_FzR5h6llK4zTy9gZjnNo4wf2@puffin.rmq2.cloudamqp.com/gllbrcms')

connection = pika.BlockingConnection(params)

channel = connection.channel()


channel.queue_declare(queue='appointment')
channel.queue_declare(queue='follow')
channel.queue_declare(queue='post')

def callback(ch, method, properties, body):
    print('Received message')
    data = json.loads(body)
    
    content_type = data.get('type')
    user_id = data.get('user_id')
    content = data.get('content')

    notification = Notification.objects.create(
        content_type=content_type,
        content=content,
        user_id=user_id,
    )
    if notification:
        print('Notification Created Successfully')
    if content_type == 'post':
        doctor_id = data.get('doctor_id')
        print("Iam readched the like Consumer rrrrrrrrrrrrrrrrrrr")
        PostNotification.objects.create(notification=notification, doctor_id=doctor_id)
    elif content_type == 'appointment':
        appointment_id = data.get('appointment_id')
        AppointmentNotification.objects.create(notification=notification, appointment_id=appointment_id)
    elif content_type == 'follow':
        followed_id = data.get('followed_id')
        FollowNotification.objects.create(notification=notification, followed_id=followed_id)
    else:
        print('Unknown message type')
    print('Enthokkeyoo Sambhavichu')
    


channel.basic_consume(queue='post', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='follow', on_message_callback=callback, auto_ack=True)
channel.basic_consume(queue='appointment', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()
print('Started Consuming')
channel.close()
