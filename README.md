# Викторина.

Ссылка на [Телеграмм бота](https://t.me/quizbrbr_bot)

В группу [VK](https://vk.com/club224005758) пришлите сообщение

Ответь на вопросы бота.
## Установка 

Установите [python3](https://realpython.com/installing-python/).

## Репозиторий
Клонируйте репозиторий в удобную папку.

## Виртуальное окружение
В терминале перейдите в папку с репозиторием.

### Создание виртуального окружения
```bush 
python3 -m venv venv
```

### Активация виртуального окружения Linux

```bush
source venv/bin/activate
```

### Активация виртуального окружения Windows

```bush
venv\Scripts\activate
```

### Установка библиотек

```bush 
pip3 install -r requirements.txt
```

#### Запись токена Telegram
```bush
echo TELEGRAM_BOT_TOKEN=ваш токен > .env
```

#### Запись токена VK
```bush
echo VK_TOKEN=ваш токен >> .env
```

### Redis
Зарегистрируйтесь на [Redis](https://redis.com/).

#### Запись REDIS_HOST
```bush
echo REDIS_HOST=ваш REDIS_HOST >> .env
```

#### Запись REDIS_PORT
```bush
echo REDIS_PORT=ваш REDIS_PORT >> .env
```

#### Запись REDIS_PASSWORD
```bush
echo REDIS_PASSWORD=ваш REDIS_PASSWORD >> .env
```

## Запуск

### Запуск ботов
Из директории с проектом выполните команды и передайте в параметры папку с вопросами.

По умолчанию вопросы хронятся в директории questions
```bush
python3 quiz.py ./questions/ 
```

Запуск бота в TG
```bush
python3 tg_bot.py
```

Запуск бота в VK
```bush
python3 vk_bot.py
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
