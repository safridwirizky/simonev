from flask import Blueprint, render_template

from services.rekomendasi_service import RekomendasiService


bp = Blueprint(
    "rekomendasi",
    __name__,
    url_prefix="/rekomendasi"
)


def get_service():

    from app import excel_service
    from app import settings_service

    return RekomendasiService(
        excel_service,
        settings_service
    )


@bp.get("/")
def index():

    service = get_service()

    table = service.table()

    return render_template(

        "rekomendasi.html",

        summary=service.summary(),

        table=table,

        total=len(table)

    )


@bp.get("/detail/<kode>")
def detail(kode):

    service = get_service()

    return render_template(

        "detail.html",

        detail=service.detail(kode)

    )
