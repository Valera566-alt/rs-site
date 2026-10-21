# Памятка по проекту IT Сервис (it150.ru)

## 🏗 Архитектура

**Движок:** Python + Flask (MVC-фреймворк)  
**Шаблоны:** Jinja2 (рендерит HTML из шаблонов + данных)  
**Стили:** CSS (только px, целые значения)  
**SEO:** Локальное — Железнодорожный, Балашиха, ул. Новая 8а  
**Домен:** www.it-150.ru → 301 → it150.ru (настраивается на уровне Nginx/прокси)

---

## 📂 Структура проекта

```
rs-site/
├── app.py              ← Маршруты (URL → функции → шаблоны)
├── services.py         ← Данные для всех страниц (JSON-структура)
├── ai_rules.md         ← Правила для ИИ-разработчика
├── requirements.txt    ← Python-зависимости
├── static/
│   ├── css/style.css   ← Все стили сайта
│   ├── img/            ← Картинки (.webp, .png)
│   ├── robots.txt      ← Запреты для поисковиков
│   └── yandex_*.html   ← Файлы верификации
├── templates/
│   ├── base.html       ← БАЗОВЫЙ ШАБЛОН (общий head, header, footer, Google-тег)
│   ├── index.html      ← Главная страница
│   ├── direction.html  ← Страницы направлений (/directions/...)
│   ├── service.html    ← Страницы услуг (/services/...)
│   ├── contacts.html   ← Контакты
│   ├── privacy.html    ← Политика конфиденциальности
│   ├── nastrojka_ecp.html ← Настройка ЭЦП
│   ├── search.html     ← Поиск по сайту
│   └── includes/
│       └── _callback_modal.html ← Модальное окно "Заказать звонок"
└── yandex_*.html       ← Файл верификации Яндекса (корень)
```

---

## 🚀 Как работает сайт (полный цикл)

### 1. Запуск сервера
```bash
python app.py
```
Flask запускает локальный сервер на **http://localhost:5001/**.

### 2. Запрос пользователя → Маршрутизация (app.py)
Пользователь вводит URL → Flask ищет совпадение в `@app.route(...)`:

| URL | Функция | Шаблон | Источник данных |
|-----|---------|--------|-----------------|
| `/` | `index()` | `index.html` | `get_site_info()` |
| `/directions/<slug>` | `direction_page(slug)` | `direction.html` | `get_site_info()` + slug |
| `/services/<slug>` | `service_page(slug)` | `service.html` | `get_site_info()` + slug |
| `/contacts` | `contacts_page()` | `contacts.html` | `get_site_info()` |
| `/privacy` | `privacy_page()` | `privacy.html` | `get_site_info()` |
| `/nastrojka-ecp` | `nastrojka_ecp_page()` | `nastrojka_ecp.html` | `get_site_info()` |
| `/search?q=...` | `search_page()` | `search.html` | `get_site_info()` + поиск |
| `/robots.txt` | `robots_txt()` | (строка в коде) | — |
| `/sitemap.xml` | `sitemap_xml()` | (строка в коде) | `get_site_info()` |

### 3. Генерация данных (services.py)
Функция `get_site_info()` возвращает **словарь со всеми данными**:
- `features` — направления (иконка, заголовок, slug, SEO-ключ, текст)
- `services` — услуги
- `steps` — этапы работы
- `faq` — вопросы-ответы
- Метаданные (phone, email, address, hours)

**Важно:** Все данные сайта хранятся в одном месте — `services.py`. Изменил здесь — обновилось везде.

### 4. Рендеринг шаблона (Jinja2)
Flask передаёт данные из `get_site_info()` в шаблон через `render_template()`.  
Jinja2 подставляет переменные (`{{ title }}`, `{{ phone }}`) и обрабатывает логику (`{% if %}`, `{% for %}`).

### 5. Ответ пользователю
Готовый HTML-файл отправляется в браузер.

---

## 🧩 Система шаблонов

### base.html — БАЗОВЫЙ ШАБЛОН (родитель)
Содержит **общий код для всех страниц**:
- `<head>` — meta-теги, Google Analytics (gtag), шрифты, CSS
- `<header>` — логотип, навигация, телефон, адрес, кнопка "Заказать звонок"
- Вторичная навигация — хлебные крошки + поиск
- `<footer>` — 4 колонки: направления, услуги, контакты, логотип
- `{% include 'includes/_callback_modal.html' %}` — модальное окно

### child-шаблоны (дети)
Каждый шаблон наследуется от `base.html`:
```jinja2
{% extends 'base.html' %}

{% block content %}
    <!-- Уникальный контент страницы -->
{% endblock %}
```

**Наследуемые шаблоны:**
- `index.html` — главная
- `direction.html` — направления
- `service.html` — услуги
- `contacts.html` — контакты
- `privacy.html` — политика
- `nastrojka_ecp.html` — настройка ЭЦП
- `search.html` — поиск

**Правило:** Изменил что-то в `base.html` → обновилось на всех страницах.

---

## 🔄 Редиректы и SEO

### 301 редирект зеркал (в коде app.py)
```python
@app.before_request
def redirect_to_main_domain():
```
- `www.it150.ru` → `it150.ru`
- `it-150.ru` → `it150.ru`
- `www.it-150.ru` → `it150.ru`
- Исключение: `/robots.txt`, `/sitemap.xml` — не редиректятся
- Работает только на VPS (не в `debug`-режиме)

### 301 редирект www → без www (настраивается Nginx/хостинг)
`www.it-150.ru` → `www.it150.ru` → `it150.ru`

---

## 🧭 Навигация (Хлебные крошки)

### Как работает
Динамическая система хлебных крошек отслеживает реальный путь пользователя по сайту через **Flask-сессии**.

**Логика работы:**
1. `track_breadcrumb_path()` — `@app.before_request` функция, которая добавляет каждый посещённый URL в сессию `session['breadcrumb_path']`
2. Сессия хранится в куках браузера (SECRET_KEY для шифрования)
3. `inject_breadcrumbs()` — `@app.context_processor`, который передаёт breadcrumbs во все шаблоны
4. `BREADCRUMB_MAP` — словарь, сопоставляющий URL с текстом для отображения

**Правила:**
- При переходе на главную `/` — история сбрасывается
- Текущая страница не дублируется (показывается некликабельной)
- Главная всегда показывается первой (кликабельной, кроме главной страницы)
- История ограничена 10 последними страницами
- Не кликабельные страницы пропускаются из кликабельного списка

**Примеры:**
- Главная: `Главная`
- `/services/remont-smartfonov`: `Главная › Ремонт смартфонов`
- `/unlock-smartphones` (через ремонт): `Главная › Ремонт смартфонов › Разблокировка смартфонов`

**Файлы:**
- `app.py` — логика (track_breadcrumb_path, inject_breadcrumbs, BREADCRUMB_MAP)
- `base.html` — шаблон рендеринга
- `style.css` — стили `.breadcrumbs`, `.breadcrumbs-item`, `.breadcrumbs-link`, `.breadcrumbs-current`

---

## 📄 Динамические страницы

### Направления (`/directions/<slug>`)
Slug берётся из `services.py` → ищется в `features` → генерируется страница.

**Примеры:**
- `/directions/razrabotka-i-prodvizhenie-sajtov` — разработка сайтов
- `/directions/pomoshch-selleram-marketplejsov` — помощь селлерам
- `/directions/kopirovalnye-uslugi-i-pechat` — копировальные услуги

**Особенные страницы направлений** (уникальный контент):
- `/directions/professionalnyj-remont` — этапы ремонта, FAQ
- `/directions/diagnostika` — диагностика разных типов техники
- `/directions/uslugi` — сетка услуг
- `/directions/remont-kompyuterov-noutbukov-monoblokov` — ремонт ПК

### Услуги (`/services/<slug>`)
Slug из `services.py` → ищется в `services` → генерируется страница.

**Особенность:** `/services/remont-smartfonov` — содержит dropdown с брендами.

---

## 📊 SEO-генераторы

### robots.txt (динамический)
`/robots.txt` → генерируется строкой в `app.py`. Содержит:
- Запрет на `/submit-callback`
- Разрешение на `/static/`
- Ссылку на `sitemap.xml`

### sitemap.xml (динамический)
`/sitemap.xml` → генерируется из данных `get_site_info()`. Содержит:
- Главная (priority 1.0)
- Все направления (priority 0.8)
- Все услуги (priority 0.8)
- `/privacy`, `/nastrojka-ecp` (priority 0.3/0.8)

### Schema.org (JSON-LD)
На главной странице (`index.html`) встроена микроразметка `LocalBusiness`:
- Адрес, телефон, email
- Геокоординаты (55.751351, 38.014282)
- График работы (ежедневно 09:00–20:00)

---

## 🎨 Стили контента

### Блок «Важно!»
Используется для выделения критически важной информации. Применяется к абзацам, начинающимся с `<strong>Важно:</strong>`.

**Стиль:**
```html
<p style="line-height: 1.6; color: #555; background: #fff3cd; padding: 16px; border-radius: 4px; border-left: 4px solid #ffc107;">
    <strong>Важно:</strong> текст...
</p>
```

**Параметры:**
- `background: #fff3cd` — песочный (светло-жёлтый) фон
- `border-left: 4px solid #ffc107` — оранжевая левая рамка (4px)
- `border-radius: 4px` — скругление углов
- `padding: 16px` — внутренние отступы
- `color: #555` — серый цвет текста
- `line-height: 1.6` — межстрочный интервал

**Где используется:**
- `nastrojka_ecp.html` — предупреждения про ФНС, сроки
- `unlock_smartphones.html` — предупреждение про подтверждение права владения

---

## 📈 Аналитика

Оба счётчика добавлены в `base.html` → работают на **всех** страницах автоматически.

### Google Analytics (gtag.js)
**ID:** `G-PHETFPKE6X`  
**Файл:** `templates/base.html` (в `<head>`)  
**Что собирает:** просмотры страниц, источники трафика, время на сайте, события, демография

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHETFPKE6X"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-PHETFPKE6X');
</script>
```

### Яндекс.Метрика
**ID:** `60302227`  
**Файл:** `templates/base.html` (в `<head>`, после Google-тега)  
**Что собирает:** просмотры страниц, карта кликов, вебвизор (запись визитов), источники трафика, поиск по сайту

```html
<!-- Yandex.Metrika counter -->
<script type="text/javascript">
   (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
   m[i].l=1*new Date();
   for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
   k=e.createElement(i),a=e.getElementsByTagName(i)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
   (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

   ym(60302227, "init", {
        clickmap:true,
        trackLinks:true,
        accurateTrackBounce:true,
        webvisor:true
   });
</script>
<noscript><div><img src="https://mc.yandex.ru/watch/60302227" style="position:absolute; left:-9999px;" alt="" /></div></noscript>
<!-- /Yandex.Metrika counter -->
```

**Включённые опции:**
- `clickmap` — карта кликов (куда нажимают пользователи)
- `trackLinks` — отслеживание переходов по ссылкам
- `accurateTrackBounce` — точный подсчёт отказов
- `webvisor` — запись визитов (видеоплеер сессий пользователей)

**Как проверить:**
- Google Analytics: открыть сайт → F12 → Console → ввести `gtag('config', 'G-PHETFPKE6X')`
- Яндекс.Метрика: открыть сайт → F12 → Console → ввести `ym(60302227, 'init')`
- Или установить расширение **Google Tag Assistant** для Chrome

---

## 🔧 Модальное окно "Заказать звонок"

**Файл:** `templates/includes/_callback_modal.html`

**Как работает:**
1. Скрипт находит все кнопки с классом `.btn-call-to-action`
2. При клике открывает модальное окно
3. Маска телефона: `+7 (XXX) XXX-XX-XX`
4. Отправка на `/submit-callback` (POST, JSON)
5. Flask отправляет сообщение через Max.ru API

**Важно:** Кнопки "Вернуться на главную" **НЕ** используют класс `btn-call-to-action` — они просто ведут на `/`.

---

## 🖼 Картинки

**Правило:** Если `icon.endswith('.webp')` → рендерится как `<img>`, иначе → эмодзи/текст.

**Путь:** `/static/img/<filename>`

**Доступные форматы:** `.webp`, `.png`

---

## 📝 Переменные шаблонов

Передаются из `app.py` через `get_site_info()`:

| Переменная | Описание |
|------------|----------|
| `title` | Заголовок страницы (SEO) |
| `tagline` | Описание страницы (meta description) |
| `phone` | Телефон |
| `email` | Email |
| `address` | Адрес |
| `hours` | График работы |
| `features` | Список направлений |
| `services` | Список услуг |
| `steps` | Этапы работы |
| `faq` | Вопросы-ответы |
| `version` | Версия сайта |
| `current_direction` | Текущее направление (slug, title, icon, text) |
| `current_service` | Текущая услуга |
| `current_breadcrumb` | Текст хлебных крошек |
| `search_query` | Запрос поиска |
| `search_results` | Результаты поиска |

---

## 🚀 Деплой на VPS

1. SSH на VPS (Ubuntu)
2. Nginx → проксирует на Flask (port 5001)
3. Flask слушает `0.0.0.0:5001`
4. SSL через Let's Encrypt / прокси

---

## 🔑 Ключевые файлы

| Файл | Назначение |
|------|------------|
| `app.py` | Маршруты, редиректы, SEO-генераторы |
| `services.py` | Все данные сайта (направления, услуги, FAQ) |
| `base.html` | Базовый шаблон (общий head, header, footer) |
| `style.css` | Все стили |
| `_callback_modal.html` | Модальное окно + маска телефона |

---

## ⚡ Быстрый чек-лист при изменении

1. **Изменить текст/данные** → `services.py`
2. **Изменить дизайн шапки/подвала** → `base.html`
3. **Изменить стили** → `static/css/style.css`
4. **Добавить новую страницу** → `app.py` (маршрут) + новый шаблон
5. **Изменить SEO-теги** → `app.py` (title, tagline)
6. **Добавить аналитику** → `base.html` (в `<head>`)
