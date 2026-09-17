from flask import Flask, render_template
from services import get_site_info

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
@app.route("/")
def index():
    # Просто передаем весь словарь в шаблон. Никаких f-string здесь быть не должно.
    return render_template("index.html", **get_site_info())

if __name__ == '__main__':
    app.run(debug=True)
