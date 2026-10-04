# Правила разработки проекта (IT сервис)

## Техническое окружение
- **ОС:** Kali Linux (русская раскладка)
- **IDE:** PyCharm 2026.2.2 
- **Стек:** Python, Flask, Jinja2, HTML, CSS (только .px)
- **Проект в сети:** www.it150.ru (301 редирект с www.it-150.ru)
- **Локальный хост:** http://localhost:5001/
- **Деплой:** Собственный VPS через SSH

## Схема взаимодействия с ИИ
1. **Общение:** Строго на русском языке. Комментарии к коду — только на русском.
2. **Шаги:** Предлагать не более 1–3 шагов по текущему вопросу.
3. **Безопасность кода:** Без уведомления пользователя НЕ МЕНЯТЬ ничего самостоятельно, не удалять файлы и не предлагать то, чего не просили.
4. **Лимиты**ПРи снижении лимита суточных запросов к тебе до 15% ты должен меня предупредить меня крупным шрифтом

┌──(fenix㉿yoga)-[~]
└─$ tree -L 4 -I '__pycache__|.git|node_modules|venv' /home/fenix/rs-site/

## Дерево файлов пректа:

/home/fenix/rs-site/
├── ai_rules.md
├── app.py
├── favicon.png
├── README.md
├── requirements.txt
├── services.py
├── static
│   ├── css
│   │   └── style.css
│   ├── img
│   │   ├── apple-touch-icon.png
│   │   ├── diagnostika.webp
│   │   ├── digital_services.webp
│   │   ├── favicon-192.png
│   │   ├── favicon.png
│   │   ├── game_console.webp
│   │   ├── headphones.webp
│   │   ├── laser.webp
│   │   ├── logo13.webp
│   │   ├── monoblock.webp
│   │   ├── pc-cooler.webp
│   │   ├── pc_laptop.webp
│   │   ├── pc_motherboard.webp
│   │   ├── pc_restor.webp
│   │   ├── pc_store.webp
│   │   ├── pc_videocard.webp
│   │   ├── remont_computerov.webp
│   │   ├── remont_tv.webp
│   │   ├── smartphone.webp
│   │   └── systems_block.webp
│   ├── robots.txt
│   └── yandex_093274bd8c7e1538.html
├── templates
│   ├── contacts.html
│   ├── direction.html
│   ├── includes
│   │   └── _callback_modal.html
│   ├── index.html
│   ├── privacy.html
│   └── service.html
└── yandex_093274bd8c7e1538.html

6 directories, 36 files


## Требования к коду и SEO
1. **Локальное SEO:** Сайт делается для привлечения клиентов в реальный сервис в МО Балашиха, мкрн. Железнодорожный, ул. Новая 8а. Оптимизация для Яндекс и Гугл должна быть заложена в каждую строчку кода.
2. **Фронтенд:** Значения `rem` и `em` недопустимы. Для адаптивности и верстки использовать строго `px` (пиксели).
3. **Цель:** Динамические SEO-лендинги под целевые запросы, блок вопросов и ответов (Q&A), калькуляторы ремонта.
