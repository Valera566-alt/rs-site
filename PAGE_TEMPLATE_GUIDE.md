# Памятка: создание шаблонной страницы (SEO-блок + Steps 4 + FAQ 6)

## Обзор шаблона

Страница использует шаблон `templates/direction.html` и общий маршрут `/directions/<slug>`.
Структура: **большой SEO-блок** → **Steps (4 карточки)** → **FAQ (6 карточек)**.

## Примеры готовых страниц

- `/directions/diagnostika-kompyuterov` — Диагностика компьютеров
- `/directions/diagnostika-smartfonov` — Диагностика смартфонов
- `/directions/remont-kompyuterov` — Ремонт компьютеров
- `/directions/diagnostika-monitorov-i-televizorov` — Диагностика мониторов и телевизоров

---

## Шаг 1: Добавить направление в `services.py`

Найти блок `features` в функции `get_site_info()` и добавить новый объект в конец списка (перед `],`):

```python
{
    "icon": "имя_файла.webp",
    "title": "Название направления",
    "slug": "nazvanie-latelinkami",
    "seo_keyword": "описание для SEO-тега (с предлогом)",
    "text": "Краткое описание для отображения на странице направлений.",
    "show_on_main": False
},
```

**Правила:**
- `icon` — имя файла из `static/img/`
- `title` — название для отображения (кириллица)
- `slug` — латиницей, слова через дефис (используется в URL)
- `seo_keyword` — описание с предлогом: "диагностике мониторов...", "ремонту компьютеров..."
- `show_on_main: False` — не показывать на главной странице

---

## Шаг 2: Добавить в `app.py`

### 2a. BREADCRUMB_MAP

Найти словарь `BREADCRUMB_MAP` и добавить строку:

```python
'/directions/НАЗВАНИЕ-SLUG': 'Название направления',
```

**Важно:** путь должен совпадать с URL `/directions/<slug>`.

### 2b. Поиск (search_page)

Найти блок `# Ищем на странице...` и добавить:

```python
# Ищем на странице НАЗВАНИЯ
search_keywords = "ключевое слово1 слово2 слово3 балашиха железнодорочный".lower()
if query in search_keywords:
    results.append({
        'type': 'Направление',
        'title': 'Название направления',
        'url': '/directions/НАЗВАНИЕ-SLUG',
        'description': 'Краткое описание для результатов поиска'
    })
```

---

## Шаг 3: Настроить шаблон `templates/direction.html`

### 3a. Добавить slug в главное условие (строка 3)

Найти строку:
```jinja2
{% if current_direction.slug == '...' or current_direction.slug == '...' %}
```

Добавить новый slug в конец через `or`:
```jinja2
... or current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
```

### 3b. Картинка в шапке (header)

Найти блок с `{% elif %}` для картинок и добавить перед `{% else %}`:

```jinja2
{% elif current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
<img src="{{ url_for('static', filename='img/ИМЯ_ФАЙЛА.webp') }}"
     alt="Описание в Железнодорожном"
     style="height: 100px; width: auto; display: block; margin: 0 auto 12px auto;">
```

### 3c. SEO-блок (большой текстовый блок)

Найти блок `{% elif current_direction.slug == '...' %}` для SEO и добавить перед `{% endif %}`:

```jinja2
{% elif current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
<h2 class="section-title" style="margin-bottom: 16px; text-align: center;">ЗАГОЛОВОК SEO-БЛОКА ВЕРХНИМ РЕГИСТРОМ</h2>
<div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border);">
    <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст первого абзаца.</p>
    <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст второго абзаца.</p>
</div>
```

**Вставка картинок в SEO-текст:**
- Картинки вставляются ВНУТРИ `<p>` с `float: left`
- Формат:
```html
<p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">
    <img src="/static/img/имя_файла.webp"
         alt="Описание"
         style="width: 200px; height: auto; float: left; margin: 0 24px 12px 0; border-radius: 8px;">
    Текст после картинки...
</p>
```
- Только px, только whole numbers (200px, 24px, 12px)

**Списки внутри SEO-блока:**
```html
<ul style="line-height: 1.8; color: #555; margin-left: 24px; margin-bottom: 16px; padding-left: 16px;">
    <li style="margin-bottom: 16px;"><strong>Заголовок пункта.</strong> Текст пункта.</li>
</ul>
```

### 3d. Заголовок Steps-блока

Найти блок заголовков `<h2 class="section-title">` и добавить перед `{% else %}`:

```jinja2
{% elif current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
<h2 class="section-title">ЗАГОЛОВОК БЛОКА ШАГОВ</h2>
```

### 3e. Steps (4 карточки)

Найти блок steps и добавить перед `{% else %}`:

```jinja2
{% elif current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
<div class="steps">
    <div class="step-item">
        <span class="step-num">1</span>
        <h3>Заголовок шага 1</h3>
        <p>Текст шага 1.</p>
    </div>
    <div class="step-item">
        <span class="step-num">2</span>
        <h3>Заголовок шага 2</h3>
        <p>Текст шага 2.</p>
    </div>
    <div class="step-item">
        <span class="step-num">3</span>
        <h3>Заголовок шага 3</h3>
        <p>Текст шага 3.</p>
    </div>
    <div class="step-item">
        <span class="step-num">4</span>
        <h3>Заголовок шага 4</h3>
        <p>Текст шага 4.</p>
    </div>
</div>
```

### 3f. FAQ (6 карточек)

Найти блок FAQ и добавить перед `{% else %}`:

```jinja2
{% elif current_direction.slug == 'НАЗВАНИЕ-SLUG' %}
<div class="faq">
    <div class="faq-item">
        <h3>Вопрос 1?</h3>
        <p>Ответ 1.</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 2?</h3>
        <p>Ответ 2.</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 3?</h3>
        <p>Ответ 3.</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 4?</h3>
        <p>Ответ 4.</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 5?</h3>
        <p>Ответ 5.</p>
    </div>
    <div class="faq-item">
        <h3>Вопрос 6?</h3>
        <p>Ответ 6.</p>
    </div>
</div>
```

---

## Шаг 4: Проверка

1. **Синтаксис Python:**
```bash
cd /home/fenix/Документы/rs-site && python3 -c "import py_compile; py_compile.compile('app.py', doraise=True); py_compile.compile('services.py', doraise=True); print('OK')"
```

2. **Страница загружается:**
```bash
sleep 3 && curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:5001/directions/НАЗВАНИЕ-SLUG
```
Должно вернуть `200`.

3. **Заглушки заменены:**
```bash
curl -s http://127.0.0.1:5001/directions/НАЗВАНИЕ-SLUG | grep -o 'Здесь будет новый контент' | wc -l
```
Для полностью заполненной страницы: `0`.

---

## ⚠️ ЧАСТЫЕ ОШИБКИ И КАК ИХ ИЗБЕЖАТЬ

### Ошибка 1: Дублирование заголовков Steps

**Проблема:** Заголовок `<h2 class="section-title">` добавляется ПРЯМО ВНУТРИ блока Steps-карточек через `{% elif %}`, вместо отдельного блока заголовков.

**Как выглядит:** На странице рендерится два заголовка Steps подряд (например, «ЭТАПЫ РЕМОНТА REDMI» + «ЭТАПЫ РЕМОНТА XIAOMI»). Причина: заголовок добавлен в неправильном месте — внутри блока `{% if %}` для Steps-карточек, а не в отдельном блоке заголовков выше.

**Как правильно:**
1. **Заголовок Steps** добавляется в блок заголовков (раздел 3d) — это отдельный `{% if %}/{% elif %}` chain ДО карточек Steps
2. **Карточки Steps** добавляются в отдельный блок `{% elif %}` — без заголовка внутри!

**Пример ПРАВИЛЬНО:**
```jinja2
<!-- БЛОК ЗАГОЛОВКОВ (раздел 3d) — ОДИН раз для всех направлений -->
{% elif current_direction.slug == 'remont-redmi' %}
<h2 class="section-title">ЭТАПЫ РЕМОНТА REDMI</h2>

<!-- БЛОК КАРТОЧЕК (раздел 3e) — ТОЛЬКО div.steps, БЕЗ h2 -->
{% elif current_direction.slug == 'remont-redmi' %}
<div class="steps">
    <div class="step-item">...</div>
    ...
</div>
```

### Ошибка 2: Дублирование заголовка внутри FAQ-блока

**Проблема:** Добавлен лишний `{% elif %}` блок с заголовком Steps внутри FAQ-секции.

**Как выглядит:** На странице появляются блоки Steps в неправильном месте (после FAQ).

**Как правильно:** Steps и FAQ — это РАЗНЫЕ секции. Steps добавляется в блок Steps, FAQ — в блок FAQ. Никогда не добавляйте Steps-карточки в FAQ-секцию и наоборот.

### Ошибка 3: Неправильная структура `{% elif %}`

**Проблема:** Каждый блок (SEO, Steps-карточки, FAQ) — это ОТДЕЛЬНЫЙ `{% elif %}`. Если добавить заголовок внутрь блока карточек, рендерятся ВСЕ заголовки подряд.

**Правило:**
- SEO-блок: `{% elif current_direction.slug == '...' %}` + h2 + div
- Steps-заголовок: `{% elif current_direction.slug == '...' %}` + h2
- Steps-карточки: `{% elif current_direction.slug == '...' %}` + div.steps
- FAQ: `{% elif current_direction.slug == '...' %}` + div.faq

Каждый блок — независимый `{% elif %}`. Заголовок НЕ вкладывается внутрь карточек.

### Ошибка 4: Дублирование slug в главном условии

**Проблема:** slug добавляется в `{% if %}` несколько раз или добавляется в неправильное место.

**Как проверить:**
```bash
grep -c 'remont-redmi' /home/fenix/Документы/rs-site/templates/direction.html
```
Должно быть ровно 4 вхождения (главное условие, шапка, SEO, Steps, FAQ).

### Ошибка 5: Пропущен `{% elif %}` между SEO-блоками — дублирование контента

**Проблема:** После `</div>` одного SEO-блока отсутствует `{% elif current_direction.slug == 'следующий-бренд' %}` перед следующим блоком. Из-за этого все последующие SEO-блоки рендерятся на КАЖДОЙ странице.

**Как выглядит:** На странице `remont-honor` или `remont-tecno` после своего SEO-блока появляется SEO-блок от `remont-realme` или любого другого бренда, идущего в шаблоне позже.

**Причина:** В цепочке `{% if %} ... {% elif %} ... {% elif %} ... {% else %} ... {% endif %}` каждый блок — независимый `{% elif %}`. Если после `</div>` предыдущего блока нет `{% elif %}` с новым slug, Jinja2 не знает, где заканчивается текущий блок, и рендерит всё, что идёт дальше.

**Как правильно:** После закрытия `</div>` каждого SEO-блока ОБЯЗАТЕЛЬНО должен стоять `{% elif current_direction.slug == 'следующий-бренд' %}` перед следующим блоком:

```jinja2
{% elif current_direction.slug == 'remont-honor' %}
<h2 class="section-title">РЕМОНТ СМАРТФОНОВ HONOR В ЖЕЛЕЗНОДОРОЖНОМ</h2>
<div style="background: var(--card-bg); padding: 40px; ...">
    <p>Контент Honor...</p>
</div>
{% elif current_direction.slug == 'remont-tecno' %}  <!-- ОБЯЗАТЕЛЬНО! -->
<h2 class="section-title">РЕМОНТ СМАРТФОНОВ TECNO В ЖЕЛЕЗНОДОРОЖНОМ</h2>
<div style="background: var(--card-bg); padding: 40px; ...">
    <p>Контент Tecno...</p>
</div>
{% elif current_direction.slug == 'remont-realme' %}  <!-- ОБЯЗАТЕЛЬНО! -->
<h2 class="section-title">РЕМОНТ СМАРТФОНОВ REALME В ЖЕЛЕЗНОДОРОЖНОМ</h2>
```

**Как проверить:**
```bash
curl -s http://127.0.0.1:5001/services/remont-tecno | grep -oE '(РЕМОНТ СМАРТФОНОВ TECNO|РЕМОНТ СМАРТФОНОВ REALME|РЕМОНТ СМАРТФОНОВ HONOR)' | sort | uniq -c
```
Должно быть `1` только для tecno, `0` для остальных.

**Золотое правило:** После каждого SEO-блока (закрытия `</div>`) в цепочке `{% elif %}` ОБЯЗАТЕЛЬНО должен стоять `{% elif current_direction.slug == 'следующий-бренд' %}` перед следующим блоком. Без него все последующие блоки рендерятся на каждой странице.

---

## Чек-лист

- [ ] Добавлен объект в `services.py` (features)
- [ ] Добавлен в `BREADCRUMB_MAP` в `app.py`
- [ ] Добавлен в поиск `search_page()` в `app.py`
- [ ] Slug добавлен в `{% if %}` (строка 3) в `direction.html`
- [ ] Добавлена картинка в шапку (elif + img)
- [ ] Добавлен SEO-блок (h2 + div + контент)
- [ ] Добавлен заголовок Steps (ОТДЕЛЬНЫЙ блок, НЕ внутри карточек!)
- [ ] Добавлены 4 карточки Steps (БЕЗ h2 внутри!)
- [ ] Добавлены 6 карточек FAQ (в отдельной секции FAQ!)
- [ ] Python синтаксис OK
- [ ] Страница возвращает 200
- [ ] Заглушки заменены на реальный текст
- [ ] **Нет дубликатов заголовков** (проверить: `grep -o 'ЭТАПЫ' | wc -l` должно быть `1`)
- [ ] **Steps и FAQ в правильных секциях** (Steps ДО FAQ, не перемешаны)

---

## Пример: диагностика мониторов и телевизоров

**slug:** `diagnostika-monitorov-i-televizorov`
**URL:** `/directions/diagnostika-monitorov-i-televizorov`
**Иконка:** `remont_tv.webp`
**Breadcrumbs:** "Диагностика мониторов и телевизоров"
**Заголовок Steps:** "ЭТАПЫ ДИАГНОСТИКИ МОНИТОРОВ И ТЕЛЕВИЗОРОВ"
**Заголовок SEO:** "ДИАГНОСТИКА МОНИТОРОВ И ТЕЛЕВИЗОРОВ В ЖЕЛЕЗНОДОРОЖНОМ"
