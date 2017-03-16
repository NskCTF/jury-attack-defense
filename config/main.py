import os

# конфигурация для MongoDB
DATABASE = {
	'HOST': 'localhost', # по умолчанию
	'PORT': 27017, # по умолчанию
	'AUTH': 'true', # если true, то нужно обязательно указать user/pass от базы. Новичкам рекомендуется оставить false
	'USER': 'USERNAME',
	'PASSWORD': 'PASSWORD'
}
# конфигурация системы проверки флагов/сервисов
CHECKER = {
	'PORT': 2605, # порт сервиса приёмки флагов
	'ROUND_LENGTH': 20, # время раунда в секундах
	'CHECK_LENGTH': 10, # интервал проверки работоспособности сервиса в секундах
	'FLAG_LENGTH': 20, # длина флага в символах
	'FLAG_PREFIX': 'NSKCTF', # префикс у флага
	'LENGTH': 4, # Время жизни флага в раундах
	'METHOD': 'queue', # метод работы системы заливки флагов round: async or queue
	'MAX_CONNECTIONS': 100, # максимальное число соединений сервиса flags
}

# конфигруация для RabbitMQ
QUEUE = {
	'HOST': 'localhost', # localhost для мастер-сервера, для остальных - real ip
	'USERNAME': 'USERNAME', # юзер для очереди (по дефолту не требуется)
	'PASSWORD': 'PASSWORD', # пароль для очереди (по дефолту не требуется)
	'QNAME': 'tasks' # название очереди
}

# конфигурация для метода взятия конфига с API
API = {
	'HOST': '10.16.255.196',
	'PORT': '5000'
}

BASE_PATH = os.path.dirname(__file__) + '/../'
