# ПАМЯТКА: Создание страницы услуги (service.html)

## Структура страницы услуги (на примере remont-systemnyh-blokov)

---

### ШАГ 1: Добавить услугу в services.py

В секции `"services"` добавить запись:

```python
{
    "title": "Название услуги",
    "slug": "nazvanie-uslugi",
    "seo_keyword": "поисковый ключ",
    "icon": "icon.webp"
},
```

---

### ШАГ 2: Добавить маршрут в app.py

**Место:** после `remont_statsionarnyh_kompyuterov_page()`

```python
@app.route("/services/<slug>")
def remont_nazvanie_page():
    """Страница услуги"""
    site_info = get_site_info()
    page_data = site_info.copy()
    page_data["title"] = "Название услуги в Железнодорожном — IT Сервис"
    page_data["tagline"] = "Краткое описание услуги."
    page_data["current_breadcrumb"] = "Название услуги"
    return render_template("nazvanie_shablon.html", **page_data)
```

**Важно:** slug уже есть в `BREADCRUMB_MAP` — проверь!

---

### ШАГ 3: Создать шаблон templates/<nazvanie>.html

**КРИТИЧЕСКИ ВАЖНО:** Шаблон ДОЛЖЕН начинаться с `{% extends 'base.html' %}`!

#### Минимальная структура:

```html
{% extends 'base.html' %}

{% block content %}

    <!-- 1. ШАПКА СТРАНИЦЫ -->
    <section class="section" style="text-align: center; padding: 20px 16px;">
        <span style="font-size: 64px; display: block; margin-bottom: 16px;">
            <img src="/static/img/icon.webp" alt="Описание" style="height: 80px; width: auto;">
        </span>
        <h1 style="font-size: 30px; margin-bottom: 24px; color: #222;">Заголовок h1</h1>
        <p style="font-size: 21px; max-width: 800px; margin: 0 auto 40px auto; color: #555; line-height: 1.6;">
            Описание услуги.<br>
        </p>
    </section>

    <!-- 2. БЛОК 50/50: 2 карточки-ссылки -->
    <section class="section" style="padding: 16px 0 32px;">
        <div style="display: flex; gap: 16px; max-width: 1200px; margin: 0 auto; align-items: stretch;">
            <!-- Левая карточка -->
            <a href="/services/ссылка" style="flex: 1; text-decoration: none; color: inherit; display: block; background: var(--card-bg); padding: 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); transition: box-shadow 0.2s;">
                <img src="/static/img/icon1.webp" alt="Описание" style="width: 120px; height: auto; float: left; margin-right: 16px; margin-bottom: 8px; border-radius: 8px;">
                <h3 style="font-size: 20px; margin-bottom: 12px; color: #222;">Заголовок</h3>
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; font-size: 16px; text-indent: 0;">Текст карточки.</p>
                <span style="color: var(--primary); font-weight: 600; font-size: 16px;">Подробнее →</span>
            </a>
            <!-- Правая карточка -->
            <a href="/services/ссылка" style="flex: 1; text-decoration: none; color: inherit; display: block; background: var(--card-bg); padding: 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); transition: box-shadow 0.2s;">
                <img src="/static/img/icon2.webp" alt="Описание" style="width: 120px; height: auto; float: left; margin-right: 16px; margin-bottom: 8px; border-radius: 8px;">
                <h3 style="font-size: 20px; margin-bottom: 12px; color: #222;">Заголовок</h3>
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; font-size: 16px; text-indent: 0;">Текст карточки.</p>
                <span style="color: var(--primary); font-weight: 600; font-size: 16px;">Подробнее →</span>
            </a>
        </div>
    </section>

    <!-- 3. SEO-БЛОКИ (5 блоков с картинками) -->
    <section class="section" id="seo-text">
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img1.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст блока 1.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img2.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст блока 2.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img3.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст блока 3.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img4.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст блока 4.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img5.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст блока 5.</p>
            </div>
        </div>
    </section>

    <!-- 4. ЭТАПЫ РЕМОНТА (4 карточки) -->
    <section class="section" id="about">
        <h2 class="section-title">ЭТАПЫ РЕМОНТА НАЗВАНИЕ</h2>
        <div class="steps">
            <div class="step-item">
                <span class="step-num">1</span>
                <h3>Заголовок этапа 1</h3>
                <p>Текст этапа 1.</p>
            </div>
            <div class="step-item">
                <span class="step-num">2</span>
                <h3>Заголовок этапа 2</h3>
                <p>Текст этапа 2.</p>
            </div>
            <div class="step-item">
                <span class="step-num">3</span>
                <h3>Заголовок этапа 3</h3>
                <p>Текст этапа 3.</p>
            </div>
            <div class="step-item">
                <span class="step-num">4</span>
                <h3>Заголовок этапа 4</h3>
                <p>Текст этапа 4.</p>
            </div>
        </div>
    </section>

    <!-- 5. FAQ (6 вопросов) -->
    <section class="section" id="faq">
        <h2 class="section-title">ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ О РЕМОНТЕ НАЗВАНИЕ</h2>
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
    </section>

</div>

{% endblock %}
```

---

### ШАГ 4: Проверка

```bash
# 1. Синтаксис Python
cd /home/fenix/Документы/rs-site && python3 -c "import py_compile; py_compile.compile('app.py', doraise=True); print('OK')"

# 2. HTTP статус
curl -s -o /dev/null -w "%{http_code}" http://localhost:5001/services/<slug>

# 3. Наличие футера
curl -s http://localhost:5001/services/<slug> | grep -c "site-footer"  # должно быть 1

# 4. Наличие шапки
curl -s http://localhost:5001/services/<slug> | grep -c "header-wrapper"  # должно быть 1

# 5. Количество заглушек (если нужно)
curl -s http://localhost:5001/services/<slug> | grep -c "Здесь будет текст"
```

---

## КРИТИЧЕСКИЕ ОШИБКИ

### ❌ ОШИБКА 1: Нет `{% extends 'base.html' %}`
**Симптом:** Нет шапки, футера, меню, стилей  
**Решение:** Первая строка шаблона ОБЯЗАТЕЛЬНО `{% extends 'base.html' %}`

### ❌ ОШИБКА 2: Нет `{% endblock %}` в конце
**Симптом:** Страница ломается, контент не рендерится  
**Решение:** В конце шаблона ОБЯЗАТЕЛЬНО `{% endblock %}`

### ❌ ОШИБКА 3: Лишний `</div>`
**Симптом:** Контент обрезается, блоки не отображаются  
**Решение:** Проверить баланс `<div>` — каждый открывающий должен быть закрыт

### ❌ ОШИБКА 4: Не тот slug в маршруте
**Симптом:** 404 Not Found  
**Решение:** Проверить slug в `@app.route()` и в `BREADCRUMB_MAP`

---

## ШАБЛОН ДЛЯ КОПИРОВАНИЯ (быстрый старт)

```html
{% extends 'base.html' %}

{% block content %}

    <section class="section" style="text-align: center; padding: 20px 16px;">
        <span style="font-size: 64px; display: block; margin-bottom: 16px;">
            <img src="/static/img/icon.webp" alt="Описание" style="height: 80px; width: auto;">
        </span>
        <h1 style="font-size: 30px; margin-bottom: 24px; color: #222;">Заголовок</h1>
        <p style="font-size: 21px; max-width: 800px; margin: 0 auto 40px auto; color: #555; line-height: 1.6;">
            Описание.<br>
        </p>
    </section>

    <section class="section" style="padding: 16px 0 32px;">
        <div style="display: flex; gap: 16px; max-width: 1200px; margin: 0 auto; align-items: stretch;">
            <a href="#" style="flex: 1; text-decoration: none; color: inherit; display: block; background: var(--card-bg); padding: 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); transition: box-shadow 0.2s;">
                <img src="/static/img/icon1.webp" alt="Описание" style="width: 120px; height: auto; float: left; margin-right: 16px; margin-bottom: 8px; border-radius: 8px;">
                <h3 style="font-size: 20px; margin-bottom: 12px; color: #222;">Заголовок</h3>
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; font-size: 16px; text-indent: 0;">Текст.</p>
                <span style="color: var(--primary); font-weight: 600; font-size: 16px;">Подробнее →</span>
            </a>
            <a href="#" style="flex: 1; text-decoration: none; color: inherit; display: block; background: var(--card-bg); padding: 32px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); transition: box-shadow 0.2s;">
                <img src="/static/img/icon2.webp" alt="Описание" style="width: 120px; height: auto; float: left; margin-right: 16px; margin-bottom: 8px; border-radius: 8px;">
                <h3 style="font-size: 20px; margin-bottom: 12px; color: #222;">Заголовок</h3>
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; font-size: 16px; text-indent: 0;">Текст.</p>
                <span style="color: var(--primary); font-weight: 600; font-size: 16px;">Подробнее →</span>
            </a>
        </div>
    </section>

    <section class="section" id="seo-text">
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img1.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img2.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img3.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img4.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст.</p>
            </div>
        </div>
        <div style="background: var(--card-bg); padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); border: 1px solid var(--border); margin-bottom: 24px;">
            <div style="display: flex; gap: 24px; align-items: flex-start;">
                <img src="/static/img/img5.webp" alt="Описание" style="width: 200px; height: auto; float: left; margin-right: 24px; margin-bottom: 12px; border-radius: 8px;">
                <p style="line-height: 1.6; color: #555; margin-bottom: 16px; text-indent: 24px;">Текст.</p>
            </div>
        </div>
    </section>

    <section class="section" id="about">
        <h2 class="section-title">ЭТАПЫ РЕМОНТА НАЗВАНИЕ</h2>
        <div class="steps">
            <div class="step-item"><span class="step-num">1</span><h3>Заголовок</h3><p>Текст.</p></div>
            <div class="step-item"><span class="step-num">2</span><h3>Заголовок</h3><p>Текст.</p></div>
            <div class="step-item"><span class="step-num">3</span><h3>Заголовок</h3><p>Текст.</p></div>
            <div class="step-item"><span class="step-num">4</span><h3>Заголовок</h3><p>Текст.</p></div>
        </div>
    </section>

    <section class="section" id="faq">
        <h2 class="section-title">ЧАСТО ЗАДАВАЕМЫЕ ВОПРОСЫ О РЕМОНТЕ НАЗВАНИЕ</h2>
        <div class="faq">
            <div class="faq-item"><h3>Вопрос 1?</h3><p>Ответ.</p></div>
            <div class="faq-item"><h3>Вопрос 2?</h3><p>Ответ.</p></div>
            <div class="faq-item"><h3>Вопрос 3?</h3><p>Ответ.</p></div>
            <div class="faq-item"><h3>Вопрос 4?</h3><p>Ответ.</p></div>
            <div class="faq-item"><h3>Вопрос 5?</h3><p>Ответ.</p></div>
            <div class="faq-item"><h3>Вопрос 6?</h3><p>Ответ.</p></div>
        </div>
    </section>

</div>

{% endblock %}
```

---

## ИТОГОВАЯ ПРОВЕРКА ПЕРЕД СДАЧЕЙ

- [ ] `{% extends 'base.html' %}` — ПЕРВАЯ СТРОКА
- [ ] `{% endblock %}` — ПОСЛЕДНЯЯ СТРОКА
- [ ] Баланс `<div>` — все открыты и закрыты
- [ ] Нет лишних `</div>`
- [ ] Python синтаксис OK
- [ ] HTTP статус 200
- [ ] Есть header-wrapper
- [ ] Есть site-footer
- [ ] 2 блока 50/50
- [ ] 5 SEO-блоков
- [ ] 4 этапа
- [ ] 6 FAQ

---

**Дата создания:** 2025  
**Версия:** 1.0
