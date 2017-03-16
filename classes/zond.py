from __future__ import print_function
import sys
import threading
import os
import pika, time, json

from bson import json_util
from functions import Message
from classes.checker.main import Checker
from config.main import QUEUE
from classes.config.get import ConfigGet

try:
    import thread
except ImportError:
    import _thread as thread


class Zond:
    thread = []

    codes = {
        101: 'UP', # means that service is online, serves the requests, stores and returns flags and behaves as expected.
        102: 'CORRUPT', # means that service is online, but past flags cannot be retrieved.
        103: 'MUMBLE', # means that service is online, but behaves not as expected, e.g. if HTTP server listens the port, but doesn't respond on request.
        104: 'DOWN' # means that service is offline.
    }

    def __init__(self, db):
        self.db = db # соединение с базой данных
        self.settings = ConfigGet(self.db).get_all_settings() # загрузка файла с настройками сервера
        self.checker = Checker() # подргружаем чекер (QUEUE or ASYNC)
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=QUEUE['HOST'],
            credentials=pika.credentials.PlainCredentials(QUEUE['USERNAME'], QUEUE['PASSWORD'])
        ))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=QUEUE['QNAME'])

        print(' [*] Waiting for messages. To exit press CTRL+C')

    def run(self):
        self.channel.basic_consume(self.callback,
                              QUEUE['QNAME'],
                              no_ack=True)
        self.channel.start_consuming()

    # данная функция срабатывает при каждом пришедшем пакете из MQTT. Идёт обработка
    def callback(self, ch, method, properties, body):
        data = json.loads(body.decode('utf8'))
        print(" [x] Received %r %r" % (data['team']['name'], data['service']['name']))

        path = self.settings['path_to_checkers'] + "/" + data['service']['name']
        #if data['action'] == 'update':
        #Message.info('\t UPDATING checker files!')
        if not os.path.exists(path):
            os.mkdir(path, mode=0o777)

        file = open(path + "/" + self.settings['filename_checkers'], 'w')
        file.write(data['service']['program'] + "\r\n")
        file.close()

        self.thread.append(threading.Thread(
            name=(data['team']['name'] + data['service']['name']),
            target=self.to_service,
            args=(data['action'], data['round'], data['team'], data['service'], data['flag'], data['flag_id']))
        )
        self.thread[-1].daemon = True
        self.thread[-1].start()

    # это тред чекера. Для каждого сервиса/команды - свой
    def to_service(self, action, round, team, service, flag, flag_id):
        team = json_util.loads(json.dumps(team))
        service = json_util.loads(json.dumps(service))

        self.db.flags.insert_one({
            'round': round,
            'team': team,
            'service': service,
            'flag': flag,
            'flag_id': flag_id,
            'stolen': False,
            'timestamp': time.time()
        })

        path = self.settings['path_to_checkers'] + '/' + service['name'] + '/' + self.settings['filename_checkers']

        try:

            if action == 'check':
                self.checker.check(team['host'], path)
            if action == 'put':
                self.checker.put(team['host'], path, flag, flag_id)
            if action == 'get':
                self.checker.get(team['host'], path, flag, flag_id)

            self.update_scoreboard(team, service, 101)

        except Exception as error:
            code, message = error.args
            print(error)
            Message.fail(team['name'] + ' ' + service['name'] + ' ' + action + ' => error (message: ' + str(message) + ')')
            self.update_scoreboard(team, service, code, message)


    def update_scoreboard(self, team, service, status_code, message=''):
        codes = {
            101: 'UP',
            102: 'CORRUPT',
            103: 'MUMBLE',
            104: 'DOWN'
        }

        # self.status_service[team['name'] + '_' + service['name']] = status_code

        if status_code not in codes:
            Message.fail('\t Invalid checker return code for ' + service['name'])
            status_code = 104

        self.db.scoreboard.update_one(
            {
                'team._id': team['_id'],
                'service._id': service['_id']
            },
            {
                "$set": {
                    "status": codes[status_code],
                    'message': message
                },
                '$inc': {
                    'up_round': 1 if status_code == 101 else 0
                }
            }
        )
