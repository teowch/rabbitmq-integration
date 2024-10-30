import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def publish_message(channel, value, routing_key):
    channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=value)
    print(f" [x] Sent {routing_key}:{value}")

def ask_and_publish(channel, routing_key, verb):
    print(f'\033[2JVai {verb}?\n')
    user_input = input("1. Sim\n2. Nao")
    value = True if user_input == '1' else (False if user_input == '2' else None)
    if value != None:
        publish_message(channel, value, routing_key)
    else:
        input("Entrada invalida. Pressione qualquer tecla para continuar...")
