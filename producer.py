import connect_mongo
from models import Contact
from faker import Faker
from random import choice
import pika

NUMBER_OF_CONTACTS = 23


def main():

    fake_data = Faker()

    for _ in range(NUMBER_OF_CONTACTS):
        Contact(
            fullname=fake_data.name(),
            email=fake_data.email(),
            phone=fake_data.phone_number(),
            contact_via=choice(["sms", "email"]),
        ).save()

    contacts = Contact.objects()

    credentials = pika.PlainCredentials("guest", "guest")
    connection_parameters = pika.ConnectionParameters(
        host="localhost", port=5672, credentials=credentials
    )
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    channel.queue_declare(queue="send_email")
    channel.queue_declare(queue="send_sms")

    for contact in contacts:
        if not contact.message_sent:
            contact_id = str(contact.id)
            target_queue = f"send_{contact.contact_via.value}"
            channel.basic_publish(
                exchange="", routing_key=target_queue, body=contact_id.encode()
            )

    connection.close()


if __name__ == "__main__":
    main()
