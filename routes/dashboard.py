from flask import Blueprint
from flask import current_app
from flask import render_template

from extensions import excel
from extensions import settings_service

from services.dashboard_service import DashboardService


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def index():

    dashboard = DashboardService(
        excel,
        settings_service
    )

    return render_template(

        "index.html",

        table=dashboard.table()

    )
