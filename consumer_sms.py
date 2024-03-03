import pika
from models import Contact
import connect_mongo
import time


def send_sms(phone_number: str) -> None:
    print(f"sending sms to: {phone_number[:3]}...")


credentials = pika.PlainCredentials("guest", "guest")
connection_parameters = pika.ConnectionParameters(
    host="localhost", port=5672, credentials=credentials
)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()

channel.queue_declare(queue="send_sms")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id)[0]
    print(f" [x] Received {contact_id}")
    send_sms(contact.phone)
    time.sleep(1)
    contact.update(message_sent=True)
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="send_sms", on_message_callback=callback)

print(" [*] Waiting for messages. To exit press CTRL+C")

if __name__ == "__main__":
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        connection.close()
        print("Disconnected from rabbit")
