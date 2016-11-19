Платформа для проведения игр CTF в формате Attack-defense
=========================================================
Автор: github.com/shipko. Выражаем большую благодарность команде keva за помощь и развитие проекта

Установка
---------
Автоматизированная установка производится на сервер с операционной системой debian или ubuntu (рекомендуется ubuntu 16.04 64-bit).

Для установки необходимо перейти в рабочий каталог проекта и запустить install.sh

    `./install.sh`

Установка на другие платформы производится вручную по аналогии.

Запуск
------
Система состоит из отдельных модулей с единой точкой входа.
Для начала необходимо проинициализировать

    `python3 main.py init --type=json`          для старта из файла-json (по умолчанию)
    `python3 main.py init --type=api`           для старта из API (нужно запустить `./api.py`)

Для запуска модулей необходимо выполнить команды:

    `python3 main.py flags`                     запуск приемки флагов
    `python3 main.py scoreboard`                запуск таблицы результатов
    `python3 main.py start`                     старт чекеров

Генератор флагов
------
flag_generator.py - утилита для генерации флагов.

    `python3 flag_generator.py [кол-во флагов] [длина флага]`

Установка MongoDB
------
Последняя версия MongoDB на данный момент 3.2.10 Ставим
```
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list     Ubuntu 14.04
echo "deb http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.2 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.2.list     Ubuntu 16.04
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo apt-get install -y mongodb-org=3.2.10 mongodb-org-server=3.2.10 mongodb-org-shell=3.2.10 mongodb-org-mongos=3.2.10 mongodb-org-tools=3.2.10

```

Конфигурирование MongoDB
------
Система требует авторизации пользователя, поэтому сделаем её.

1. Заходим в MongoDB командой `mongo`
2. Открываем БД администраторов `use admin`
3. Создаём учётку такой командой:
```
db.createUser(
   {
     user: "USER",
     pwd: "PASSWORD",
     roles:
       [
         { role: "readWrite", db: "jury" },
         "clusterAdmin"
       ]
   }
)
```

4. Останавливаем MongoDB `service mongodb stop` (я просто убивал через _pkill_)
5. Запускаем MongoDB с параметром _--auth_: `mongod --auth --dbPath=/path/do/db`
6. Авторизация включена!
```

Конфигурация RabbitMQ
------
RabbitMQ - брокер сообщений (сервер и платформа для обмена сообщениями между компонентами программной среды). Он необходим, когда платформа работает в режиме **queue**

Требования: Ubuntu 14.04-16.04 64-bit

```
echo 'deb http://www.rabbitmq.com/debian/ testing main' |
    sudo tee /etc/apt/sources.list.d/rabbitmq.list
wget -O- https://www.rabbitmq.com/rabbitmq-release-signing-key.asc |
    sudo apt-key add -
sudo apt-get update
sudo apt-get install -yq rabbitmq-server
```
