import pika
from models import Contact
import connect_mongo
import time


def send_email(email_address: str) -> None:
    print(f"sending email to: {email_address[:3]}...")


credentials = pika.PlainCredentials("guest", "guest")
connection_parameters = pika.ConnectionParameters(
    host="localhost", port=5672, credentials=credentials
)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue="send_email")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id)[0]
    print(f" [x] Received {contact_id}")
    send_email(contact.email)
    time.sleep(1)
    contact.update(message_sent=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="send_email", on_message_callback=callback)

print(" [*] Waiting for messages. To exit press CTRL+C")

if __name__ == "__main__":
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print("Disconnected from rabbit")
