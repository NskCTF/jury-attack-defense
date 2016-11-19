import pika, json
from bson import json_util
from config.main import QUEUE

class Queue:
    list = []
    def __init__(self):
        # Устанавливаем соединение
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=QUEUE['HOST']
#            credentials=pika.credentials.PlainCredentials(QUEUE['USERNAME'], QUEUE['PASSWORD'])
        ))
        self.channel = connection.channel()

        self.channel.queue_declare(queue=QUEUE['QNAME'])

    def send(self):
        pass

    def put(self, **kwargs):
        self.list.append(kwargs)

    def run(self):
        for task in self.list:
            self.channel.basic_publish(
                exchange='',
                routing_key=QUEUE['QNAME'],
                body=json.dumps(task, default=json_util.default)
            )
            print('Sended')

    def clear(self):
        # Если вдруг у нас задания не отправились в очередь
        self.list = []
        # Очищаем очередь, если задания остались
        self.channel.queue_purge(queue=QUEUE['QNAME'])
