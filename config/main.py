import os

# конфигурация для MongoDB
DATABASE = {
	'HOST': 'localhost', # по умолчанию
	'PORT': 27017, # по умолчанию
	'AUTH': 'false', # если true, то нужно обязательно указать user/pass от базы. Новичкам рекомендуется оставить false
	'USER': 'USER',
	'PASSWORD': 'PASSWORD'
}
# конфигурация системы проверки флагов/сервисов
CHECKER = {
	'PORT': 2605, # порт сервиса приёмки флагов
	'ROUND_LENGTH': 60, # в секундах
	'LENGTH': 4, # Время жизни флага в раундах
	'METHOD': 'queue' # async or queue
}

# конфигруация для RabbitMQ
QUEUE = {
	'HOST': 'localhost', # localhost для мастер-сервера, для остальных - real ip
	'USERNAME': 'user', # юзер для очереди (по дефолту не требуется)
	'PASSWORD': 'StrongPassword', # пароль для очереди (по дефолту не требуется)
	'QNAME': 'tasks' # название очереди
}

# конфигурация для метода взятия конфига с API
API = {
	'HOST': '10.16.255.196',
	'PORT': '5000'
}

BASE_PATH = os.path.dirname(__file__) + '/../'
