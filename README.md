# Python Meetup Bot
Бот для организации митапов на тему Python-разработки.


## Пример бота
Доступен по ссылке в Телеграм: 


## Запуск
- Рекомендуется использовать виртуальное окружение для запуска проекта
- Для корректной работы Вам необходим Python версии 3.6 и выше
- API-ключ для работы с Telegram-ботом (инструкция [тут](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html)).
- Скачайте код (`git clone`)
- Установите зависимости командой
```bash
pip install -r requirements.txt
```
- Для запуска админ-панели необходимо выполнить команду:
```bash
python manage.py runserver
```
- Для запуска Telegram-бота необходимо выполнить команду:
```bash
python manage.py startbot
```


## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, 
создайте файл `.env` в корневой директории проекта и запишите туда данные в таком 
формате: `ПЕРЕМЕННАЯ=значение`.

Доступные переменные:

- `TG_BOT_APIKEY` - Ваш API-ключ для работы с Telegram-ботом
- `DEBUG` — дебаг-режим. Поставьте `False`.
- `SECRET_KEY` — секретный ключ проекта. Он отвечает за шифрование на сайте. Например, им зашифрованы все пароли на вашем сайте. Ключ можно получить [тут](https://djecrety.ir/)
- `ALLOWED_HOSTS` — [см. документацию Django](https://docs.djangoproject.com/en/3.1/ref/settings/#allowed-hosts)


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).