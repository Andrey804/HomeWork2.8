import faker
import pika
from models import Contacts
import connect


NUMBER_CONTACTS = 5


def add_contacts():

    fake_data = faker.Faker()

    # Contacts.drop_collection()

    for _ in range(NUMBER_CONTACTS):
        Contacts(fullname=fake_data.name(), email=fake_data.email(),
                 phone=[fake_data.unique.phone_number() for _ in range(fake_data.random_int(1, 3))],
                 sending_preference=fake_data.random_element(['email', 'phone'])).save()


def main():

    creds = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=creds))
    channel = connection.channel()

    channel.queue_declare(queue='contacts_pref_email')
    channel.queue_declare(queue='contacts_pref_phone')

    for contact in Contacts.objects(is_send=False):

        if contact.sending_preference == 'phone':
            channel.basic_publish(exchange='', routing_key='contacts_pref_phone', body=str(contact.id).encode())

        else:
            channel.basic_publish(exchange='', routing_key='contacts_pref_email', body=str(contact.id).encode())

    connection.close()


if __name__ == '__main__':

    add_contacts()
    main()
