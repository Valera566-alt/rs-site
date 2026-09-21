from flask import Flask, render_template, abort
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

    # Перезаписываем title и tagline под конкретную локальную услугу в Железнодорожном
    page_data["title"] = f"{current_service['title']} в Железнодорожном — цены на ул. Новая 8а"
    page_data[
        "tagline"] = f"Профессиональный {current_service['seo_keyword']} в сервисном центре в Железнодорожном. Быстрая диагностика, честные цены и гарантия!"

    # Добавляем в словарь данные о текущей открытой услуге, чтобы вывести её текст на лендинге
    page_data["current_service"] = current_service

    # Передаем обновленные данные в отдельный чистый шаблон лендинга услуги
    return render_template("service.html", **page_data)


if __name__ == '__main__':
    app.run(debug=True)
