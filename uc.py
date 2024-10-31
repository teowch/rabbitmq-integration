import sys, os
import sd_common
import threading
import pika
import logging
from signature import sign_message, verify_message, get_private_key, get_public_key
from keygen import create_key_pair
import json


conn1 = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
conn2 = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = conn1.channel()
channel2 = conn2.channel()
irrigation_lock = threading.Lock()
condition_event = threading.Event()

chuva = False
geada = False
umidade = 20.0

old_chuva = chuva
old_geada = geada
old_umidade = umidade

def handle_message(ch, method, properties, body):
    global chuva
    global geada
    global umidade
    global old_chuva
    global old_geada
    global old_umidade

    routing_key = method.routing_key

    if routing_key == 'meteorologia.chuva':
        chuva = eval(body)
        print(f" [x] chuva={chuva}")
    elif routing_key == 'meteorologia.geada':
        geada = eval(body)
        print(f" [x] geada={geada}")
    elif routing_key == 'umidade':
        umidade = float(body)
        print(f" [x] umidade={umidade}")
    
    if (old_chuva != chuva or old_geada != geada or old_umidade != umidade):
        old_chuva = chuva
        old_geada = geada
        old_umidade = umidade
        print(f" [x] New values: chuva={chuva}, geada={geada}, umidade={umidade}")
        condition_event.set()


def callback(ch, method, properties, body):
    payload = json.loads(body)
    message = payload['message']
    signature = payload['signature']

    routing_key = method.routing_key
    print(f"Received message from routing key: {routing_key}: {payload}")

    pub_keyname = "pub_meteorologia" if routing_key.startswith("meteorologia") else "pub_sensor" if routing_key == "umidade" else "pub_uc"
    
    if verify_message(message, signature, get_public_key(pub_keyname)):
        print(f" [x] Mensagem recebida e verificada.")
        handle_message(ch, method, properties, message)
    else:
        print(f" [x] Mensagem recebida, mas a assinatura é inválida")


def consumer_thread():
    print("consumer_thread    : started")
    global channel

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=sd_common.exchange_name, queue=queue_name, routing_key='meteorologia.*')
    channel.queue_bind(exchange=sd_common.exchange_name, queue=queue_name, routing_key='umidade')

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
            

def producer_thread():
    print("producer_thread    : started")
    routing_key="irrigacao"
    global channel2
    umidade_threshold = 20.0
    global chuva
    global geada
    global umidade
    channel2 = sd_common.connection.channel()


    while True:
        condition_event.wait()
        condition_event.clear()
        print("An event has been set")
        should_irrigate = not chuva and ((umidade < umidade_threshold) or geada) 
        print(f" [x] Should irrigate: {should_irrigate}")

        value_bytes = str(should_irrigate).encode('utf-8')
        signature = sign_message(value_bytes, get_private_key("pk_uc"))

        payload = {
            "message": value_bytes.decode('utf-8'),
            "signature": signature.hex()
        }

        channel2.basic_publish(
                exchange=sd_common.exchange_name, routing_key=routing_key, body=json.dumps(payload))
        print(f" [x] Sent {routing_key}:{should_irrigate}")

def main():
    create_key_pair("pk_uc", "pub_uc")
    global channel

    channel.exchange_declare(exchange=sd_common.exchange_name, exchange_type='topic')

    #consumer = threading.Thread(target=consumer_thread, daemon=True)
    producer = threading.Thread(target=producer_thread, daemon=True)
    logging.info("Main    : before running thread")
    #consumer.start()
    producer.start()
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
