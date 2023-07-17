import pika
from models import Contacts
import connect


creds = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=creds))
channel = connection.channel()

channel.queue_declare(queue='contacts_pref_phone')


def callback(ch, method, properties, body):
    contacts = Contacts.objects(id=body.decode())

    for contact in contacts:
        print(f'Send message to one of phone: {[phone for phone in contact.phone]}')

    ch.basic_ack(delivery_tag=method.delivery_tag)
    contacts.update_one(is_send=True)


channel.basic_consume(queue='contacts_pref_phone', on_message_callback=callback)

if __name__ == '__main__':
    channel.start_consuming()
