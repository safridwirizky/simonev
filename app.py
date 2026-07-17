from flask import Flask
from flask_bootstrap import Bootstrap5

from config import Config

from routes.api import api_bp
from routes.dashboard import dashboard_bp
from routes.rekomendasi import bp as rekomendasi_bp

from extensions import excel_service
from extensions import settings_service

from services.dashboard_service import DashboardService

bootstrap = Bootstrap5()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    bootstrap.init_app(app)

    excel_service.load(app.config["EXCEL_FILE"])

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(rekomendasi_bp)

    return app


app = create_app()

print(excel_service.realisasi.head())

print()

print(excel_service.anggaran.head())

'''
@dashboard_bp.route("/")
def index():

    dashboard = DashboardService(
        excel_service,
        settings_service
    )
'''

if __name__ == "__main__":
    app.run(debug=True)
