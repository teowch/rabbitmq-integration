import pika
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

with open("private_key.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(key_file.read(), password=None)

def sign_message(message, private_key):
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='events_exchange', exchange_type='topic')

message = b"Evento importante gerado pelo publicador"
signature = sign_message(message, private_key)

payload = {
    "message": message.decode('utf-8'),
    "signature": signature.hex()
}

channel.basic_publish(exchange='events_exchange', routing_key='event.important', body=json.dumps(payload))

print(" [x] Mensagem enviada")
connection.close()
