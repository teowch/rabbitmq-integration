import sys, os
import sd_common
import threading
import logging
from signature import verify_message, get_public_key
from keygen import create_key_pair
import json

channel = sd_common.connection.channel()

def callback(ch, method, properties, body):
    payload = json.loads(body)
    message = payload['message']
    signature = payload['signature']

    routing_key = method.routing_key
    print(f"Received message from routing key: {routing_key}: {payload}")
    
    pub_keyname = "pub_uc"
    pub_key = get_public_key(pub_keyname)

    if verify_message(message, signature, pub_key):
        print(f" [x] Mensagem recebida e verificada.")
        if (eval(message)):
            print(f" [x] Abrindo válvula")
        else:
            print(f" [x] Fechando válvula")

    else:
        print(f" [x] Mensagem recebida, mas a assinatura é inválida")

    


def consumer_thread():
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=sd_common.exchange_name, queue=queue_name, routing_key='irrigacao')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    

def main():
    create_key_pair("pk_valvula", "pub_valvula")
    
    channel.exchange_declare(exchange=sd_common.exchange_name, exchange_type='topic')
    consumer_thread()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sd_common.connection.close()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
