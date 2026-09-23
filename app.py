from flask import Flask, render_template, abort, request, jsonify
import requests  # Библиотека для пересылки вебхуков в Макс мессенджер
from services import get_site_info

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def index():
    # Главная страница: распаковываем все базовые данные (включая стандартные title и tagline)
    return render_template("index.html", **get_site_info())


@app.route("/services/<slug>")
def service_page(slug):
    # Получаем базовый словарь с данными сайта
    site_info = get_site_info()

    # Ищем конкретную услугу, которую запросил пользователь по ссылке (slug)
    current_service = None
    for service in site_info['services']:
        if service['slug'] == slug:
            current_service = service
            break

    # Если такой услуги нет в базе данных, отдаем стандартную ошибку 404
    if not current_service:
        abort(404)

    # Создаем копию словаря, чтобы безопасно переопределить SEO-теги под Яндекс
    page_data = site_info.copy()

    # Перезаписываем title и tagline под конкретную локальную услугу
    page_data["title"] = f"{current_service['title']} в Железнодорожном — IT Сервис"
    page_data[
        "tagline"] = f"Профессиональный {current_service['seo_keyword']} в сервисном центре в Железнодорожном. Быстрая диагностика, честные цены и гарантия!"

    # Добавляем в словарь данные о текущей открытой услуге, чтобы вывести её текст на лендинге
    page_data["current_service"] = current_service

    # Передаем обновленные данные в отдельный чистый шаблон лендинга услуги
    return render_template("service.html", **page_data)


@app.route("/directions/<slug>")
def direction_page(slug):
    # Получаем исходные данные сайта
    site_info = get_site_info()

    # Ищем, какое именно из 4 направлений открыл пользователь
    current_direction = None
    for feature in site_info['features']:
        if feature['slug'] == slug:
            current_direction = feature
            break

    # Если направление не найдено в списке, отдаем стандартную ошибку 404
    if not current_direction:
        abort(404)

    # Создаем копию данных сайта для безопасной подмены SEO-тегов под Яндекс
    page_data = site_info.copy()

    # Точечное SEO с жесткой локальной привязкой к Железнодорожному и Балашихе
    page_data["title"] = f"{current_direction['title']} в Железнодорожном | IT Сервис"
    page_data[
        "tagline"] = f"Услуги по {current_direction['seo_keyword']} в оригинальном сервисном центре на ул. Новая 8a. Звоните: {site_info['phone']}!"

    # Передаем маркер текущего открытого направления
    page_data["current_direction"] = current_direction

    # Рендерим отдельную шаблонную страницу направления
    return render_template("direction.html", **page_data)


# РОУТ ПРИЁМА ЗАЯВКИ: Пересылает имя и телефон клиента в мессенджер МАКС
@app.route("/submit-callback", methods=["POST"])
def submit_callback():
    data = request.get_json()
    if not data or 'name' not in data or 'phone' not in data:
        return jsonify({"success": False, "error": "Неполные данные"}), 400

    client_name = data['name']
    client_phone = data['phone']

    # Текст лида для отправки на ваш рабочий аккаунт
    message_text = (
        f"🚨 НОВАЯ ЗАЯВКА С САЙТА it150.ru!\n\n"
        f"👤 Имя клиента: {client_name}\n"
        f"📞 Телефон: {client_phone}\n"
        f"📍 Локация: мкр. Железнодорожный"
    )

    # ВШИТЫЙ БОЕВОЙ ТОКЕН И ID ПОЛУЧАТЕЛЯ
    BOT_TOKEN = "f9LHodD0cOLb4_aiv1mUeV2QhSthPNmzFLzT-_dtpIjei5hOXJvo2Fko7droG2G06vPZP9CESvhY-vWbimuB"
    YOUR_USER_ID = "se14421641"

    # Базовый эндпоинт отправки текстовых сообщений Bot API МАКС (VK Teams / MyTeam)
    API_URL = "https://max.ru"

    params = {
        "token": BOT_TOKEN,
        "chatId": YOUR_USER_ID,
        "text": message_text
    }

    try:
        # Отправляем HTTPS-запрос с VPS сервера в МАКС мессенджер
        response = requests.get(API_URL, params=params, timeout=5)
        result = response.json()

        # Если сервер МАКС успешно принял запрос и доставил лид в чат
        if response.ok and result.get('ok', False):
            return jsonify({"success": True})
        else:
            print(f"Ошибка API МАКС: {result}")
            return jsonify({"success": False, "error": "Ошибка мессенджера"}), 500

    except Exception as e:
        print(f"Критическая ошибка сети на VPS Ubuntu: {e}")
        return jsonify({"success": False, "error": "Ошибка сервера"}), 500


if __name__ == '__main__':
    # Слушаем порт 5001, так как его жестко требует прокси-конфиг Nginx на VPS
    app.run(host='0.0.0.0', port=5001, debug=True)
