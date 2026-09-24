import os
import requests  # Библиотека для пересылки вебхуков в Макс мессенджер
from flask import Flask, render_template, abort, request, jsonify, redirect
from services import get_site_info

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.before_request
def redirect_to_main_domain():
    """SEO-склейка зеркал: безопасный редирект 301 на главное окно it150.ru (без www)"""
    if app.debug:
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


@app.route("/")
def index():
    # Главная страница: распаковываем все базовые данные
    return render_template("index.html", **get_site_info())


@app.route("/services/<slug>")
def service_page(slug):
    site_info = get_site_info()
    current_service = None
    for service in site_info['services']:
        if service['slug'] == slug:
            current_service = service
            break

    if not current_service:
        abort(404)

    page_data = site_info.copy()
    page_data["title"] = f"{current_service['title']} в Железнодорожном — IT Сервис"
    page_data[
        "tagline"] = f"Профессиональный ремонт {current_service['seo_keyword']} в сервисном центре в Железнодорожном. Быстрая диагностика, честные цены и гарантия!"
    page_data["current_service"] = current_service

    return render_template("service.html", **page_data)


@app.route("/directions/<slug>")
def direction_page(slug):
    site_info = get_site_info()
    current_direction = None
    for feature in site_info['features']:
        if feature['slug'] == slug:
            current_direction = feature
            break

    if not current_direction:
        abort(404)

    page_data = site_info.copy()
    page_data["title"] = f"{current_direction['title']} в Железнодорожном | IT Сервис"
    page_data[
        "tagline"] = f"Услуги по {current_direction['seo_keyword']} в профессиональном сервисном центре на ул. Новая 8a. Звоните: {site_info['phone']}!"
    page_data["current_direction"] = current_direction

    return render_template("direction.html", **page_data)


@app.route("/submit-callback", methods=["POST"])
def submit_callback():
    data = request.get_json()
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"success": False, "error": "Неполные данные"}), 400

    client_name = data['name']
    client_phone = data['phone']

    message_text = (
        f"🚨 НОВАЯ ЗАЯВКА С САЙТА it150.ru!\n\n"
        f"👤 Имя клиента: {client_name}\n"
        f"📞 Телефон: {client_phone}\n"
        f"📍 Локация: мкр. Железнодорожный"
    )

    BOT_TOKEN = "f9LHodD0cOLb4_aiv1mUeV2QhSthPNmzFLzT-_dtpIjei5hOXJvo2Fko7droG2G06vPZP9CESvhY-vWbimuB"
    USER_ID = "21641785"
    API_URL = "https://max.ru"

    headers = {
        "Authorization": BOT_TOKEN,
        "Content-Type": "application/json"
    }
    params = {"user_id": USER_ID}
    body = {"text": message_text}

    try:
        response = requests.post(
            API_URL,
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
    """Отдаем robots.txt поисковым роботам напрямую из папки static"""
    return app.send_static_file('robots.txt')


@app.route('/sitemap.xml')
def sitemap_xml():
    """Динамическая генерация sitemap.xml для Яндекса и Google"""
    from flask import make_response
    import datetime

    site_info = get_site_info()
    base_url = "https://it150.ru"
    now = datetime.datetime.now().strftime('%Y-%m-%d')

    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += f'<urlset xmlns="http://sitemaps.org">\n'

    # 1. Главная страница
    xml_content += f'  <url><loc>{base_url}/</loc><lastmod>{now}</lastmod><priority>1.0</priority></url>\n'

    # 2. Страницы направлений
    for feature in site_info['features']:
        xml_content += f'  <url><loc>{base_url}/directions/{feature["slug"]}</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>\n'

    # 3. Страницы услуг
    for service in site_info['services']:
        xml_content += f'  <url><loc>{base_url}/services/{service["slug"]}</loc><lastmod>{now}</lastmod><priority>0.8</priority></url>\n'

    xml_content += f'</urlset>'

    response = make_response(xml_content)
    response.headers["Content-Type"] = "application/xml"
    return response


@app.route('/yandex_093274bd8c7e1538.html')
def yandex_verification():
    """Отдаем проверочный файл Яндекса из папки static, но по корневому адресу"""
    return app.send_static_file('yandex_093274bd8c7e1538.html')




if __name__ == '__main__':
    # Слушаем порт 5001, так как его жестко требует прокси-конфиг Nginx на VPS
    app.run(host='0.0.0.0', port=5001, debug=True)
