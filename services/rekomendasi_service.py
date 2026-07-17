from services.analytics_service import AnalyticsService


class RekomendasiService:

    def __init__(self, excel_service, settings_service):

        self.excel = excel_service
        self.settings = settings_service

    @property
    def analytics(self):

        return AnalyticsService(
            self.excel.realisasi,
            self.excel.anggaran,
            self.settings
        )

    def detail(self, kode):

        return self.analytics.get_detail(kode)

    def summary(self):

        rows = self.table()

        summary = {

            "total": len(rows),

            "belum": 0,

            "diproses": 0,

            "selesai": 0

        }

        for row in rows:

            status = row["status"]

            if status == "Belum Ditindaklanjuti":

                summary["belum"] += 1

            elif status == "Diproses":

                summary["diproses"] += 1

            elif status == "Selesai":

                summary["selesai"] += 1

        return summary

    def table(self):

        rows = []

        for item in self.analytics.get_sub_kegiatan():

            detail = self.analytics.get_detail(
                item["kode"]
            )

            evaluasi = detail.get("evaluasi")

            if not evaluasi:
                continue

            rekomendasi = evaluasi.get(
                "rekomendasi"
            )

            if not rekomendasi:
                continue

            tindak_lanjut = (
                detail.get("tindak_lanjut")
                or {}
            )

            rows.append({

                **item,

                "rekomendasi": rekomendasi,

                "status": tindak_lanjut.get(
                    "status",
                    "-"
                ),

                "badge": tindak_lanjut.get(
                    "badge",
                    "bg-secondary"
                )

            })

        return rows
