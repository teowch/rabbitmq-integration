import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def publish_message(channel, value, routing_key):
    channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=value)
    print(f" [x] Sent {routing_key}:{value}")

def publish_will_occur(channel, routing_key):
    value = input("1. Sim\n2. Nao")
    if('1' == value):
        publish_message(channel, "True", routing_key)
    elif('2' == value):
        publish_message(channel, "False", routing_key)
    else:
        print("opcao invalida")