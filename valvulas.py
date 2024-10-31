import sys, os
import sd_common
import threading
import logging

channel = sd_common.connection.channel()

def callback(ch, method, properties, body):
    payload = body.decode('utf-8')
    routing_key = method.routing_key
    print(f"Received message from routing key: {routing_key}: {payload}")
    #message = payload['message']
    #signature = payload['signature']
    
    """ if verify_message(message, signature, public_key):
        print(f" [x] Mensagem recebida e verificada: {message}")
    else:
        print(f" [x] Mensagem recebida, mas a assinatura é inválida") """
    
    if (eval(payload)):
        print(f" [x] Abrindo válvula")
    else:
        print(f" [x] Fechando válvula")


def consumer_thread():
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=sd_common.exchange_name, queue=queue_name, routing_key='irrigacao')
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    

def main():
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
