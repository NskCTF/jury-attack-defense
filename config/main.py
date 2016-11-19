import os

DATABASE = {
	'HOST': 'localhost',
	'PORT': 27017,
	'USER': 'USER',
	'PASSWORD': 'PASSWORD'
}
#
CHECKER = {
	'ROUND_LENGTH': 60, # в секундах
	'LENGTH': 4, # Время жизни флага в раундах
	'METHOD': 'queue' # async or queue
}

# конфигруация для RabbitMQ
QUEUE = {
	'HOST': 'localhost',
	'USERNAME': 'user',
	'PASSWORD': 'StrongPassword',
	'QNAME': 'tasks'
}

# конфигурация для метода взятия конфига с API
API = {
	'HOST': '10.16.255.196',
	'PORT': '5000'
}

BASE_PATH = os.path.dirname(__file__) + '/../'
