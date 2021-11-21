# СК Ладный
Сеть складов для частных лиц в Моске


*Сайт сети складов представляет упорядоченное описание услуг и преимуществ. Основной функционал: получить стоимость аренды площади или сезонного хранения вещей в зависимости от срока аренды и локации и оформить заказ на аренду. *

![Скриншот приложения](selfstorage.png)

[Демо-версия](http://89.108.64.81/)



## Установка

Приложение является свободным, ты можешь установить его и пользоваться. Для этого тебе понадобятся:
1. Python 3.6+ [см. как установить (англ.)](https://realpython.com/installing-python/), а [здесь для Debian-based (рус.)](http://userone.ru/?q=node/41).
2. Django 3.x [см. как установить (рус.)](https://developer.mozilla.org/ru/docs/Learn/Server-side/Django/development_environment).

Далее, скачай репозиторий к себе, установи и активируй виртуальное окружение: 

    python3 -m venv env
    source env/bin/activate

установи необходимые библиотеки для Django, указанные в файле requirements.txt:

    pip install -r requirements.txt

запусти сайт:

    ./manage.py runserver

и открой его в браузере, указав в адресной строке (главная страница или административная панель):

    http://127.0.0.1:8000
    http://127.0.0.1:8000/admin


Фронтенд представляет собой готовый шаблон. В качестве карты используется [Яндекс.Карты](https://www.yandex.ru/maps). Для работы шаблона используются следующие javascript- и css-библиотеки:


* [Bootstrap](https://getbootstrap.com/) — CSS библиотека


Всё включено и настроено :)

## Переменные окружения

Для улучшения уровня безопасности, когда будешь размещать сайт в общем доступе, сделай файл .env и размести его в папке проекта. В этом файле укажи секретный ключ Django, желательно не менее 50 символов. Сгенерировать ключ можно с помощью генераторов паролей, который в интернете очень много. Вот так должен выглядеть твой .env файл:

    DEBUG=false
    SECRET_KEY='длинная строка символов'

Указывать этот ключ в файле настроек settings.py не нужно.

 

## Роли

### Администратор сайта

Администратор сайта является суперпользователем, имеет все права в отношении контента. На демо-сайте авторизуйся со следующими данными:

    Логин: admin
    Пароль: admin

###

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).



