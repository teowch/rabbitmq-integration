import pika
import sys, os
import sd_common
import json 
from signature import sign_message, get_private_key
from keygen import create_key_pair

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def main():
    print("\033[2J")
    channel = connection.channel()

    channel.exchange_declare(exchange=sd_common.exchange_name, exchange_type='topic')
    routing_key = 'umidade'

    create_key_pair("pk_sensor", "pub_sensor")

    while(True):
        value = input("Leitura de umidade: ")
        if(float(value) < 0 or float(value) > 100):
            print("Valor de umidade inválido")
            continue

        value_bytes = value.encode('utf-8') 
        signature = sign_message(value_bytes, get_private_key("pk_sensor"))

        payload = {
            "message": value,
            "signature": signature.hex()
        }
        
        channel.basic_publish(
            exchange=sd_common.exchange_name, routing_key=routing_key, body=json.dumps(payload))
        print(f" [x] Sent {routing_key}:{value}\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        connection.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
