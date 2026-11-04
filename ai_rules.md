# Правила разработки проекта (IT сервис)

## Техническое окружение
- **ОС:** Dibian Trixi 13.7 (русская раскладка)
- **IDE:** PyCharm 2026.2.2 (русская раскладка)
- **Стек:** Python, Flask, Jinja2, HTML, CSS (только .px и только целые значения пикселей без дробных)
- **Проект в сети:** www.it150.ru (301 редирект с www.it-150.ru)
- **Локальный хост:** http://localhost:5001/
- **Деплой:** Собственный VPS через SSH

## Схема взаимодействия с ИИ
Ты — Senior Fullstack разработчик. Мы пишем локальный SEO-сайт для сервисного центра в Железнодорожном (ул. Новая 8а).
1. **Общение:** Строго на русском языке. Комментарии к коду — только на русском.
2. **Шаги:** Предлагать не более 1–3 шагов по текущему вопросу.
3. **Безопасность кода:** Без уведомления пользователя НЕ МЕНЯТЬ ничего самостоятельно, не удалять файлы и не предлагать то, чего не просили.

## Требования к коду и SEO
1. **Локальное SEO:** Сайт делается для привлечения клиентов в реальный сервис в МО Балашиха, мкрн. Железнодорожный, ул. Новая 8а. Оптимизация для Яндекс и Гугл должна быть заложена в каждую строчку кода.
2. **Фронтенд:** Значения `rem` и `em` недопустимы. Для адаптивности и верстки использовать строго `px` (пиксели).
3. **Цель:** Динамические SEO-лендинги под целевые запросы, блок вопросов и ответов (Q&A), калькуляторы ремонта.

## Архитектура шаблонов
- **base.html** — базовый шаблон (head, header, footer, счётчики аналитики, хлебные крошки, поиск)
- **direction.html** — шаблон направлений (`/directions/<slug>`) с conditional-блоками для special-страниц
  - Special-направления: `professionalnyj-remont`, `diagnostika`, `uslugi`, `remont-kompyuterov-noutbukov-monoblokov`, `razrabotka-i-prodvizhenie-sajtov`, `pomoshch-selleram-marketplejsov`, `kopirovalnye-uslugi-i-pechat`
  - Каждое special-направление имеет: Hero-секцию, SEO-текст, этапы работы, FAQ
- **service.html** — шаблон услуг (`/services/<slug>`) с conditional-блоками
  - Special-услуги: `remont-smartfonov` (dropdown брендов, блоки 50/50), `remont-systemnyh-blokov`
- Статические страницы: `/unlock-smartphones`, `/nastrojka-ecp`, `/contacts`, `/privacy` — отдельные шаблоны

## Система поиска (search_page)
- **Где находится:** `app.py`, функция `search_page()`
- **Как работает:** Ищет запрос по нескольким источникам (case-insensitive, по подстроке)
- **Источники поиска:**
  1. **Направления (features):** `title + seo_keyword + text`
  2. **Услуги (services):** `title + seo_keyword`
  3. **Статические страницы:** ручной поисковый текст для каждой страницы
     - `/contacts` — контакты, адрес, телефон
     - `/nastrojka-ecp` — настройка ЭЦП, Рутокен, КриптоПро, ФНС
     - `/unlock-smartphones` — разблокировка, пароль, FRP, iPhone, Samsung, Xiaomi
     - `/directions/pomoshch-selleram-marketplejsov` — селлеры, Wildberries, Ozon, КриптоПро, этикетки
     - `/directions/razrabotka-i-prodvizhenie-sajtov` — разработка сайтов, лендинг, SEO
     - `/directions/kopirovalnye-uslugi-i-pechat` — копировальные услуги, печать, ксерокопия
     - `/services/remont-systemnyh-blokov` — ремонт ПК, диагностика, комплектующие
     - `/services/remont-smartfonov` — ремонт смартфонов, замена экрана, аккумулятора
- **Правила добавления:** После блока поиска по услугам, перед `page_data = site_info.copy()`
- **Структура добавления:**
  ```python
  page_search = "ключевое слово 1 ключевое слово 2 ...".lower()
  if query in page_search:
      results.append({
          'type': 'Страница'|'Направление'|'Услуга',
          'title': 'Отображаемый заголовок',
          'url': '/url-страницы',
          'description': 'Краткое описание'
      })
  ```

## Хлебные крошки (Breadcrumbs)
- **Механиз:** Сессионная навигация через `session['breadcrumb_path']`
- **Логика:** `@app.before_request` отслеживает каждый URL → `@app.context_processor` передаёт во все шаблоны
- **BREADCRUMB_MAP:** Словарь сопоставления URL с текстом для отображения
- **Правила:**
  - При переходе на `/` — история сбрасывается
  - Текущая страница не кликабельна
  - Главная всегда первая
  - Максимум 10 последних страниц
- **Файлы:** `app.py` (логика + BREADCRUMB_MAP), `base.html` (рендеринг)

## Статические страницы (не из services.py)
- **Определение:** Страницы с уникальным контентом, который не хранится в `services.py`
- **Примеры:**
  - `/unlock-smartphones` — разблокировка смартфонов (SEO-текст, этапы, FAQ)
  - `/nastrojka-ecp` — настройка ЭЦП и Рутокенов
  - `/services/diagnostika-systemnyh-blokov` — диагностика ПК
  - `/services/remont-statsionarnyh-kompyuterov` — ремонт стационарных ПК
  - `/services/remont-smartfonov-detail` — детальное описание ремонта смартфонов
- **Правила:**
  - Маршрут в `app.py` → функция → `render_template()`
  - SEO-контент в отдельном шаблоне
  - **Обязательно:** Добавить поисковый текст в `search_page()`

## SEO-генераторы
- **robots.txt:** Динамический, генерируется строкой в `app.py` (`/robots.txt`)
- **sitemap.xml:** Динамический, генерируется из `get_site_info()` (`/sitemap.xml`)
  - Включает: главная, все направления, все услуги, privacy, nastrojka-ecp
  - **Важно:** Новые страницы из `services.py` автоматически добавляются в sitemap
- **Schema.org JSON-LD:** На главной — микроразметка `LocalBusiness` (адрес, телефон, координаты, график)

## Модальные окна и формы
- **Callback-модалка:** `templates/includes/_callback_modal.html`
- **Логика:** Кнопки с классом `.btn-call-to-action` → модальное окно → маска телефона `+7 (XXX) XXX-XX-XX` → POST на `/submit-callback` → отправка через Max.ru API
- **Важно:** Обычные кнопки (например "Вернуться на главную") НЕ используют класс `btn-call-to-action`

## CSS-правила
- **Единственный файл:** `static/css/style.css`
- **Единицы измерения:** Только `px` (целые значения), без `rem`, `em`, `%` для размеров
- **Переменные:** CSS-переменные в `:root` (цвета, отступы, шрифты)
- **Специальные стили:** Блок "Важно!" — песочный фон + оранжевая левая рамка (см. SITE_GUIDE.md)

## Аналитика
- **Google Analytics (gtag.js):** ID `G-PHETFPKE6X` — в `<head>` base.html
- **Яндекс.Метрика:** ID `60302227` — в `<head>` base.html (clickmap, trackLinks, accurateTrackBounce, webvisor)
- Оба счётчика работают на всех страницах автоматически через `base.html`

## Ключевые файлы проекта
| Файл | Назначение |
|------|------------|
| `app.py` | Маршруты, редиректы, хлебные крошки, поиск, SEO-генераторы |
| `services.py` | Все данные сайта (features, services, steps, faq, мета-данные) |
| `base.html` | Базовый шаблон (head, header, footer, аналитика) |
| `direction.html` | Шаблон направлений (conditional для special-страниц) |
| `service.html` | Шаблон услуг (dropdown брендов, блоки 50/50) |
| `unlock_smartphones.html` | Страница разблокировки смартфонов |
| `diagnostika_systemnyh_blokov.html` | Диагностика системных блоков |
| `remont_systemnyh_blokov.html` | Ремонт стационарных компьютеров |
| `remont_smartfonov_detail.html` | Детальный ремонт смартфонов |
| `style.css` | Все стили сайта |
| `_callback_modal.html` | Модальное окно заказа звонка

## Создание страницы типа "Диагностика компьютеров" (SEO + Этапы + FAQ)

### Общая структура
Страница с тремя основными блоками:
1. **Hero-секция** — заголовок + описание (автоматически из direction.html)
2. **SEO-текст** — большой блок с текстом и встроенными картинками (float: left)
3. **Этапы работы** — 4 карточки с нумерацией
4. **FAQ** — 6 карточек с вопросами и ответами

### Шаг 1: Добавление в services.py
```python
{
    "icon": "systems_block.webp",  # или другая картинка из static/img/
    "title": "Название направления",
    "slug": "slug-napravleniya",
    "seo_keyword": "SEO-ключевая фраза",
    "text": "Краткое описание для карточки на главной",
    "show_on_main": False
},
```

### Шаг 2: Добавление в BREADCRUMB_MAP (app.py)
```python
'/directions/slug-napravleniya': 'Название направления',
```

### Шаг 3: Добавление в conditional блока direction.html
В строке 3 direction.html добавить slug в условие:
```jinja2
{% if current_direction.slug == 'professionalnyj-remont' or current_direction.slug == 'diagnostika' or ... or current_direction.slug == 'slug-napravleniya' %}
```

### Шаг 4: SEO-текст (внутри блока `{% if current_direction.slug == 'slug-napravleniya' %}`)

**Структура SEO-блока:**
```jinja2
{% if current_direction.slug == 'slug-napravleniya' %}
<section class="section" id="seo-text" style="margin-bottom: 32px;">
    <h2 class="section-title" style="margin-bottom: 16px; text-align: center;">ЗАГОЛОВОК SEO-ТЕКСТА</h2>
    <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border);">
        <!-- Абзац с картинкой внутри (float: left) -->
        <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">
            <img src="/static/img/kartinka1.webp" alt="Описание картинки" style="width: 200px; height: auto; float: left; margin: 0 24px 12px 0; border-radius: 8px;">
            Текст абзаца, который обтекает картинку слева.
        </p>

        <!-- Заголовок по центру -->
        <h3 style="font-size: 22px; margin: 32px 0 16px; color: #222; text-align: center;">Подзаголовок</h3>
        <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст абзаца...</p>

        <!-- Список -->
        <ul style="line-height: 1.8; color: #555; margin-left: 24px; margin-bottom: 16px; padding-left: 16px;">
            <li style="margin-bottom: 8px;"><strong>Пункт списка:</strong> описание...</li>
        </ul>

        <!-- Вторая картинка внутри абзаца -->
        <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">
            <img src="/static/img/kartinka2.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin: 0 24px 12px 0; border-radius: 8px;">
            Текст с обтеканием картинки.
        </p>

        <!-- Заголовок с clear: both если после картинки -->
        <h3 style="font-size: 22px; margin: 32px 0 16px; color: #222; text-align: center; clear: both; display: block;">Следующий подзаголовок</h3>
    </div>
</section>
{% endif %}
```

**Правила для SEO-текста:**
- Картинки вставляются **внутрь абзаца** `<p>`, а НЕ перед заголовком
- Картинки обтекаются текстом: `float: left; margin: 0 24px 12px 0;`
- Заголовки `h3`, `h4` выравниваются по центру: `text-align: center`
- Если после картинки идёт заголовок — добавляем `clear: both; display: block`
- Все стили inline (только px, целые значения)
- **Не добавляй картинки, если пользователь не просит**

### Шаг 5: Блок "Этапы работы" (4 карточки)
```jinja2
{% elif current_direction.slug == 'slug-napravleniya' %}
<div class="steps">
    <div class="step-item">
        <span class="step-num">1</span>
        <h3>Название этапа 1</h3>
        <p>Текст описания первого этапа...</p>
    </div>
    <div class="step-item">
        <span class="step-num">2</span>
        <h3>Название этапа 2</h3>
        <p>Текст описания второго этапа...</p>
    </div>
    <div class="step-item">
        <span class="step-num">3</span>
        <h3>Название этапа 3</h3>
        <p>Текст описания третьего этапа...</p>
    </div>
    <div class="step-item">
        <span class="step-num">4</span>
        <h3>Название этапа 4</h3>
        <p>Текст описания четвертого этапа...</p>
    </div>
</div>
```

**Правила для этапов:**
- Всегда 4 карточки
- Каждая карточка: `step-item` → `step-num` (число) → `h3` (заголовок) → `p` (текст)
- Заголовок секции: `<h2 class="section-title">ЭТАПЫ [НАЗВАНИЕ]</h2>`

### Шаг 6: Блок FAQ (6 карточек)
```jinja2
{% elif current_direction.slug == 'slug-napravleniya' %}
<div class="faq">
    <div class="faq-item">
        <h3>Вопрос 1?</h3>
        <p>Ответ на первый вопрос...</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 2?</h3>
        <p>Ответ на второй вопрос...</p>
    </div>
    <!-- ... ещё 4 вопроса ... -->
    <div class="faq-item">
        <h3>Вопрос 6?</h3>
        <p>Ответ на шестой вопрос...</p>
    </div>
</div>
```

**Правила для FAQ:**
- Всегда 6 карточек
- Каждая карточка: `faq-item` → `h3` (вопрос) → `p` (ответ)
- Вопросы должны быть SEO-оптимизированы (содержать ключевые слова)

### Шаг 7: Добавить заголовок секции этапов
```jinja2
{% elif current_direction.slug == 'slug-napravleniya' %}
<h2 class="section-title">НАЗВАНИЕ СЕКЦИИ ЭТАПОВ</h2>
```

### Шаг 8: Добавить поиск (app.py)
```python
page_search = "ключевое слово 1 ключевое слово 2 ...".lower()
if query in page_search:
    results.append({
        'type': 'Направление',
        'title': 'Название направления',
        'url': '/directions/slug-napravleniya',
        'description': 'Краткое описание'
    })
```

### Итоговый чек-лист
- [ ] Добавлен feature в services.py
- [ ] Добавлен slug в BREADCRUMB_MAP
- [ ] Добавлен slug в conditional direction.html (строка 3)
- [ ] Добавлен SEO-текст с картинками (float: left внутри абзацев)
- [ ] Добавлен блок этапов (4 карточки)
- [ ] Добавлен блок FAQ (6 карточек)
- [ ] Добавлен заголовок секции этапов
- [ ] Добавлен поиск в app.py
- [ ] Проверены названия картинок в static/img/
