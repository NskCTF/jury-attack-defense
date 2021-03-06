from config.main import CHECKER
from functions import Message
from classes.checker.threads import Threads
from classes.statistic import Statistic
from classes.config.get import ConfigGet

import random
import string
import pymongo

class Round:
    db = {}
    round_count = 0

    def __init__(self, db):
        self.db = db
        self.config = ConfigGet(self.db)
        self.statistic = Statistic(self.db, self.config)
        self.status_service = {}

        if CHECKER['METHOD'] == 'queue':
            from classes.checker.queue import Queue
            self.checkerManager = Queue()
        else:
            self.checkerManager = Threads()

        Message.info('Get last round number')
        self.get_round_number()
        Message.info('\t Last round number - ' + str(self.round_count))

    def nextPut(self):
        #TODO: косяк в status_service
        # Подводим итоги предыдущего раунда

        self.statistic.summary(self.round_count)
        # Очищаем предыдущие задачи
        self.checkerManager.clear()
        self.round_count += 1

        Message.success('Round: ' + str(self.round_count))

        for team in self.config.get_all_teams():
            for service in self.config.get_all_services():
                flag = self.generate_flags()
                flag_id = self.generate_flag_ids()

                Message.info(team['name'] + ' ' + service['name'] + ' ' + flag)

                self.checkerManager.put(
                    team = team,
                    service = service,
                    flag = flag,
                    flag_id = flag_id,
                    round = self.round_count,
                    action = 'put'
                )
        self.checkerManager.run()

    def nextCheck(self):

        Message.success('Check availability of services... ')

        for team in self.config.get_all_teams():
            for service in self.config.get_all_services():

                self.checkerManager.put(
                    team = team,
                    service = service,
                    flag = None,
                    flag_id = None,
                    round = self.round_count,
                    action = 'check'
                )
        self.checkerManager.run()

    # метод генерации флага. Состоит из префикса (настраивается в конфиге), суффикса (рандомная строка N символов) и постфикса (=)
    def generate_flags(self):
        return CHECKER['FLAG_PREFIX'] + ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(CHECKER['FLAG_LENGTH'])) + '='

    def generate_flag_ids(self):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in range(10))

    # Получаем номер раунда
    def get_round_number(self):
        self.round_count = self.db.flags.find().sort([('round', pymongo.DESCENDING)]).limit(1)
        self.round_count = self.round_count[0]['round'] if self.round_count.count() else 0
