from flask import Blueprint, jsonify, request

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


@api_bp.post("/settings/triwulan")
def update_triwulan():

    data = request.get_json()

    triwulan = int(data["triwulan"])

    settings_service.set_triwulan(triwulan)

    return "", 204
