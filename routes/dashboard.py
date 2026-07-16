from flask import Blueprint, render_template

from extensions import excel_service, settings_service

from services.dashboard_service import DashboardService


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def index():

    dashboard = DashboardService(
        excel_service,
        settings_service
    )

    return render_template(
        "index.html",
        table=dashboard.table(),
        total=excel_service.total_sub_kegiatan
    )


@dashboard_bp.route("/sub-kegiatan/<kode>")
def detail(kode):

    dashboard = DashboardService(
        excel_service,
        settings_service
    )

    return render_template(
        "detail.html",
        detail=dashboard.detail(kode)
    )
