import sys, os
from sd_common import ask_and_publish, connection
import sd_common

def main():
    channel = connection.channel()
    channel.exchange_declare(exchange=sd_common.exchange_name, exchange_type='topic')

    while(True):
        print("1. Chuva\n2. Geada\n")
        value = str(input("Selecione: "))
        if('1' == value):
            ask_and_publish(channel, routing_key="meteorologia.chuva", verb="chover")
        elif('2' ==  value):
            ask_and_publish(channel, routing_key="meteorologia.geada", verb="gear")
        else:
            input("Entrada invalida. Pressione qualquer tecla para continuar...")
        print("\033[2J")


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
