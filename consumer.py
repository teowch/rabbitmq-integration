import pika
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

with open("public_key.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

def verify_message(message, signature, public_key):
    try:
        public_key.verify(
            bytes.fromhex(signature),
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Falha na verificação da assinatura: {e}")
        return False

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='events_exchange', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='events_exchange', queue=queue_name, routing_key='event.important')

print(" [*] Aguardando mensagens...")

def callback(ch, method, properties, body):
    payload = json.loads(body)
    message = payload['message']
    signature = payload['signature']
    
    if verify_message(message, signature, public_key):
        print(f" [x] Mensagem recebida e verificada: {message}")
    else:
        print(f" [x] Mensagem recebida, mas a assinatura é inválida")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
