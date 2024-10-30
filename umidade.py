import pika
import sys, os

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def main():
    channel = connection.channel()

    channel.exchange_declare(exchange='farm', exchange_type='topic')
    routing_key = 'umidade'

    while(True):
        value = input("Leitura de umidade: ") 
        if(float(value) < 0 or float(value) > 100):
            print("Valor de umidade inválido")
            continue
    
        channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=value)
        print(f" [x] Sent {routing_key}:{value}")


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
