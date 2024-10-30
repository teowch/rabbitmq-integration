import sys, os
import sd_common
import threading
import logging

channel = sd_common.connection.channel()
channel.exchange_declare(exchange='farm', exchange_type='topic')

def consumer_thread():
    logging.info("consumer_thread    : started")
    pass

def producer_thread():
    logging.info("producer_thread    : started")
    
    pass

def main():
    consumer = threading.Thread(target=consumer_thread, args=(1,), daemon=True)
    producer = threading.Thread(target=producer_thread, args=(1,), daemon=True)
    logging.info("Main    : before running thread")
    consumer.start()
    producer.start()


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
