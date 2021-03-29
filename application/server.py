from flask import Flask
from config import Config
app = Flask(__name__)
def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    app.config["JSON_AS_ASCII"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config.from_object("config.Config")

    return app

app = create_app()

from applicant_app.views import applicant_app
app.register_blueprint(applicant_app, url_prefix="/applicant_app")

from company_app.views import company_app
app.register_blueprint(company_app, url_prefix="/company_app")

from common_app.views import common_app
app.register_blueprint(common_app)

if __name__ == "__main__":
    app.run()