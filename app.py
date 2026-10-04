import os
import requests
from typing import Dict, Any, Optional
from flask import Flask, render_template, abort, request, jsonify, redirect, send_from_directory
from services import get_site_info


app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.before_request
def redirect_to_main_domain():
    """SEO-склейка зеркал: безопасный редирект 301 на главное окно it150.ru (без www)"""
    if app.debug:
        return None

    # ИСКЛЮЧЕНИЕ: отдаем robots.txt и sitemap.xml сразу, игнорируя редиректы хостов
    if request.path in ['/robots.txt', '/sitemap.xml']:
        return None

    # Читаем оригинальный хост, который Nginx перенаправил во Flask
    real_host = request.headers.get('X-Forwarded-Host') or request.headers.get('Host', '')

    # Убираем порт, если он прикрепился (например, :5001)
    if real_host:
        real_host = real_host.split(':')[0]

    # Если запрос внутренний или пустой, не трогаем его
    if not real_host or real_host in ['127.0.0.1', 'localhost']:
        return None

    # Если пользователь или робот зашли с www.it150.ru, it-150.ru или www.it-150.ru
    if real_host != 'it150.ru':
        # Жестко склеиваем на главное рабочее зеркало без www
        main_url = f"https://it150.ru{request.path}"
        if request.query_string:
            main_url += f"?{request.query_string.decode('utf-8')}"
        return redirect(main_url, code=301)

    return None

@app.route('/favicon.png')
def favicon():
    return send_from_directory(os.getcwd(), 'favicon.png', mimetype='image/png')
@app.route("/")
def index():
    # Главная страница: распаковываем все базовые данные
    return render_template("index.html", **get_site_info())


@app.route("/services/<slug>")
def service_page(slug: str):
    site_info = get_site_info()
    current_service: Optional[Dict[str, Any]] = None
    for service in site_info.get('services', []):
        if service['slug'] == slug:
            current_service = service
            break

    if not current_service:
        abort(404)

    assert current_service is not None

    page_data = site_info.copy()
    page_data["title"] = f"{current_service['title']} в Железнодорожном — IT Сервис"
    page_data["tagline"] = f"Профессиональный ремонт {current_service['seo_keyword']} в сервисном центре в Железнодорожном. Быстрая диагностика, честные цены и гарантия!"
    page_data["current_service"] = current_service

    return render_template("service.html", **page_data)


@app.route("/directions/<slug>")
def direction_page(slug: str):
    site_info = get_site_info()
    current_direction: Optional[Dict[str, Any]] = None
    for feature in site_info.get('features', []):
        if feature['slug'] == slug:
            current_direction = feature
            break

    if not current_direction:
        abort(404)

    assert current_direction is not None

    page_data = site_info.copy()
    page_data["title"] = f"{current_direction['title']} в Железнодорожном | IT Сервис"
    page_data[
        "tagline"] = f"Услуги по {current_direction['seo_keyword']} в профессиональном сервисном центре на ул. Новая 8a. Звоните: {site_info.get('phone', '')}!"
    page_data["current_direction"] = current_direction

    # Специальные данные для страницы "Профессиональный ремонт" и "Диагностика"
    if slug in ["professionalnyj-remont", "diagnostika"]:
        page_data["steps"] = [
            {"num": "1", "title": "Диагностика", "text": "Мастер осматривает устройство, выявляет неисправность и определяет стоимость ремонта."},
            {"num": "2", "title": "Согласование цены", "text": "Сообщаем вам точную стоимость и сроки ремонта. Работаем только после вашего согласия."},
            {"num": "3", "title": "Выполнение ремонта", "text": "Заменяем неисправные детали на оригинальные или сертифицированные аналоги. Проверяем работоспособность."},
            {"num": "4", "title": "Выдача с гарантией", "text": "Выдаём устройство с гарантийным талоном. Гарантия на работы от 6 месяцев."},
        ]
        page_data["faq"] = [
            {"q": "Какие виды техники вы ремонтируете?", "a": "Ремонтируем системные блоки, ноутбуки, моноблоки, смартфоны, планшеты, мониторы, телевизоры, наушники и гарнитуры."},
            {"q": "Сколько стоит диагностика?", "a": "Стоимость диагностики от 850 рублей. Если вы согласитесь на ремонт, стоимость диагностики вычитается из общей суммы ремонта."},
            {"q": "Какая гарантия на ремонт?", "a": "Гарантия на работы от 6 месяцев. Срок зависит от типа заменяемой детали и характера поломки."},
            {"q": "Делаете ли ремонт в день обращения?", "a": "Да, большинство неисправностей устраняем в день обращения. Сложные случаи занимают 1-3 дня."},
            {"q": "Используете ли оригинальные запчасти?", "a": "Используем оригинальные запчасти и сертифицированные аналоги. Все детали с гарантией от производителя."},
            {"q": "Можно ли оставить технику на хранение?", "a": "Да, храним технику до 30 дней бесплатно. После этого взимается плата за хранение."},
        ]

    # Специальные данные для страницы "Услуги"
    if slug == "uslugi":
        page_data["steps"] = [
            {"num": "1", "title": "Обращение", "text": "Вы приносите технику или оставляете заявку на сайте. Мастер принимает заказ и фиксирует проблему."},
            {"num": "2", "title": "Диагностика", "text": "Проводим бесплатную диагностику и определяем стоимость работ. Согласуем с вами цену и сроки."},
            {"num": "3", "title": "Выполнение работ", "text": "Ремонтируем, настраиваем или модернизируем технику. Используем качественные комплектующие."},
            {"num": "4", "title": "Сдача работы", "text": "Выдаём готовое устройство с гарантией. Объясняем, что было сделано и как пользоваться."},
        ]
        page_data["faq"] = [
            {"q": "Какие услуги вы оказываете?", "a": "Ремонт компьютеров и ноутбуков, диагностика, установка Windows и Linux, чистка от пыли, модернизация, настройка сетей, удаление вирусов."},
            {"q": "Сколько стоит диагностика?", "a": "Диагностика бесплатная при согласии на ремонт. Если вы откажетесь от ремонта, стоимость диагностики от 850 рублей."},
            {"q": "Какая гарантия на работы?", "a": "Гарантия на ремонтные работы от 6 месяцев, на установку ПО от 3 месяцев. Гарантийный талон выдаётся на все виды услуг."},
            {"q": "Работаете ли с организациями?", "a": "Да, обслуживаем частных клиентов и организации. Предоставляем договоры, счета и акты выполненных работ."},
            {"q": "Можно ли вызвать мастера на дом?", "a": "Да, выезд мастера на дом в Железнодорожном и Балашихе. Стоимость выезда зависит от расстояния и типа работ."},
            {"q": "Делаете ли вы модернизацию компьютеров?", "a": "Да, модернизируем системные блоки и ноутбуки: устанавливаем SSD, увеличиваем объём оперативной памяти, меняем видеокарты и процессоры."},
        ]
        # Добавляем services для отображения на странице Услуги
        page_data["services"] = site_info.get("services", [])

    return render_template("direction.html", **page_data)


@app.route("/submit-callback", methods=["POST"])
def submit_callback():
    data = request.get_json()
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"success": False, "error": "Неполные данные"}), 400

    client_name = data.get('name', '')
    client_phone = data.get('phone', '')

    message_text = (
        f"🚨 НОВАЯ ЗАЯВКА С САЙТА it150.ru!\n\n"
        f"👤 Имя клиента: {client_name}\n"
        f"📞 Телефон: {client_phone}\n"
        f"📍 Локация: мкр. Железнодорожный"
    )

    bot_token = "f9LHodD0cOLb4_aiv1mUeV2QhSthPNmzFLzT-_dtpIjei5hOXJvo2Fko7droG2G06vPZP9CESvhY-vWbimuB"
    user_id = "21641785"
    api_url = "https://platform-api2.max.ru/messages"

    headers = {
        "Authorization": bot_token,
        "Content-Type": "application/json"
    }
    params = {"user_id": user_id}
    body = {"text": message_text}

    try:
        response = requests.post(
            api_url,
            headers=headers,
            params=params,
            json=body,
            verify='/etc/ssl/certs/ca-certificates.crt',
            timeout=10
        )
        if response.ok:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": "Ошибка мессенджера"}), 500
    except requests.exceptions.SSLError as e:
        print(f"🔒 SSL-ошибка: {e}")
        return jsonify({"success": False, "error": "SSL сертификат"}), 500
    except Exception as e:
        print(f"Критическая ошибка сети на VPS Ubuntu: {e}")
        return jsonify({"success": False, "error": "Ошибка сервера"}), 500


@app.route('/robots.txt')
def robots_txt():
    """Динамически отдаем оптимизированный текст robots.txt напрямую из кода без редиректов"""
    from flask import make_response

    # Формируем контент единой чистой строкой, как в sitemap.xml
    txt_content = (
        "User-agent: Yandex\n"
        "Disallow: /submit-callback\n"
        "Allow: /static/\n"
        "Sitemap: https://it150.ru/sitemap.xml\n"
        "\n"
        "User-agent: Googlebot\n"
        "Disallow: /submit-callback\n"
        "Allow: /static/\n"
        "Sitemap: https://it150.ru/sitemap.xml\n"
        "\n"
        "User-agent: *\n"
        "Disallow: /submit-callback\n"
        "Sitemap: https://it150.ru/sitemap.xml"
    )

    response = make_response(txt_content)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


@app.route('/sitemap.xml')
def sitemap_xml():
    """Динамическая генерация sitemap.xml для Яндекса и Google"""
    from flask import make_response
    import datetime

    site_info = get_site_info()
    base_url = "https://it150.ru"
    now = datetime.datetime.now().strftime('%Y-%m-%d')

    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n'
    # noinspection HttpUrlsUsage - стандартный namespace sitemap, не сетевой запрос
    xml_content += f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

    # 1. Главная страница
    xml_content += f'  <url><loc>{base_url}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>\n'

    # 2. Страницы направлений
    for feature in site_info.get('features', []):
        if feature:
            xml_content += f'  <url><loc>{base_url}/directions/{feature["slug"]}</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>\n'

    # 3. Страницы услуг
    for service in site_info.get('services', []):
        if service:
            xml_content += f'  <url><loc>{base_url}/services/{service["slug"]}</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>\n'

    # 4. Страница политики конфиденциальности
    xml_content += f'  <url><loc>{base_url}/privacy</loc><lastmod>{now}</lastmod><priority>0.3</priority></url>\n'

    # 5. Страница настройки ЭЦП и Рутокенов
    xml_content += f'  <url><loc>{base_url}/nastrojka-ecp</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>\n'

    xml_content += f'</urlset>'

    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/yandex_093274bd8c7e1538.html')
def yandex_verification():
    """Отдаем проверочный файл Яндекса из папки static, но по корневому адресу"""
    return app.send_static_file('yandex_093274bd8c7e1538.html')

@app.route("/google969b44c74adecf16.html")
def google_verification():
    # Отдаем роботу именно ту строчку, которую он ожидает увидеть внутри файла
    return "google-site-verification: google969b44c74adecf16.html"

@app.route("/contacts")
def contacts_page():
    """Страница контактов сервисного центра с гео-SEO оптимизацией"""
    site_info = get_site_info()
    page_data = site_info.copy()

    # Формируем строго локальные SEO-метатеги под Яндекс и Google
    page_data["title"] = "Контакты сервисного центра в Железнодорожном — ул. Новая 8а"
    page_data[
        "tagline"] = f"Адрес: {site_info.get('address', '')} (ТЦ 'Корона'). Телефон: {site_info.get('phone', '')}. График работы: {site_info.get('hours', '')}. Схема проезда и контакты."

    return render_template("contacts.html", **page_data)


@app.route("/privacy")
def privacy_page():
    """Страница политики конфиденциальности с SEO-оптимизацией"""
    site_info = get_site_info()
    page_data = site_info.copy()

    # Формируем SEO-метатеги для страницы политики конфиденциальности
    page_data["title"] = "Политика конфиденциальности и обработки персональных данных — IT Сервис"
    page_data["tagline"] = "Политика конфиденциальности IT Сервис. Сбор и обработка персональных данных клиентов сервисного центра в Железнодорожном."

    return render_template("privacy.html", **page_data)


@app.route("/nastrojka-ecp")
def nastrojka_ecp_page():
    """Страница настройки ЭЦП и Рутокенов"""
    site_info = get_site_info()
    page_data = site_info.copy()

    # Формируем SEO-метатеги для страницы настройки ЭЦП
    page_data["title"] = "Настройка ЭЦП и Рутокенов в Железнодорожном — IT Сервис"
    page_data["tagline"] = "Профессиональные услуги по подключению и настройке ЭЦП и Рутокен в Железнодорожном. Установка КриптоПро, настройка сертификатов."

    return render_template("nastrojka_ecp.html", **page_data)


if __name__ == '__main__':
    # Слушаем порт 5001, так как его жестко требует прокси-конфиг Nginx на VPS
    app.run(host='0.0.0.0', port=5001, debug=True)
