import pika

exchange_name = 'farm'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

def publish_message(channel, value, routing_key):
    channel.basic_publish(
            exchange=exchange_name, routing_key=routing_key, body=value)
    print(f" [x] Sent {routing_key}:{value}")

def ask_and_publish(channel, routing_key, verb):
    print(f'\033[2JVai {verb}?\n')
    user_input = input("1. Sim\n2. Nao\n")
    value = True if user_input == '1' else (False if user_input == '2' else None)
    if value != None:
        print(f" [x] {verb} = {value}")
        publish_message(channel, str(value), routing_key)
    else:
        input("Entrada invalida. Pressione qualquer tecla para continuar...")
