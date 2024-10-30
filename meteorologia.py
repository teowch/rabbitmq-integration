import sys, os
import sd_common

def main():
    channel = sd_common.connection.channel()
    channel.exchange_declare(exchange='farm', exchange_type='topic')

    while(True):
        print("1. Chuva\n2. Geada\n")
        value = str(input("Selecione: "))
        if('1' == value):
            print('\033[2JVai chover?\n')
            sd_common.publish_will_occur(channel, routing_key="chuva")
        elif('2' ==  value):
            print('\033[2JVai gear?\n')
            sd_common.publish_will_occur(channel, routing_key="geada")
        else:
            input("Entrada invalida. Pressione qualquer tecla para continuar...")
        print("\033[2J")


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
