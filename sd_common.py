import pika
from signature import sign_message, get_private_key
from keygen import create_key_pair
import json

exchange_name = 'farm'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def publish_message(channel, value, routing_key):
    channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=value)
    print(f" [x] Sent {routing_key}:{value}")

def ask_and_publish(channel, routing_key: str, verb: str, private_key_filename: str):
    print(f'\033[2JVai {verb}?\n')
    user_input = input("1. Sim\n2. Nao\n")
    value = True if user_input == '1' else (False if user_input == '2' else None)
    if value != None:
        print(f" [x] {verb} = {value}")
        
        value_bytes = str(value).encode('utf-8')
        signature = sign_message(value_bytes, get_private_key(private_key_filename))

        payload = {
            "message": str(value),
            "signature": signature.hex()
        }

        publish_message(channel, json.dumps(payload), routing_key)
    else:
        input("Entrada invalida. Pressione qualquer tecla para continuar...")
