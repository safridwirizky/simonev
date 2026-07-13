from flask import Blueprint
from flask import jsonify
from flask import request

from extensions import settings_service

api_bp = Blueprint(
    "api",
    __name__
)


@api_bp.get("/settings")
def settings():

    return jsonify({

        "tahun": settings_service.tahun,

        "triwulan": settings_service.triwulan

    })


@api_bp.post("/settings")
def update_settings():

    data = request.get_json()

    settings_service.set_period(

        data["tahun"],

        data["triwulan"]

    )

    return jsonify({

        "success": True

    })
