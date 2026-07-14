from services.analytics_service import AnalyticsService


class DashboardService:

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

    def table(self):

        rows = []

        for item in self.analytics.get_sub_kegiatan():

            rows.append({

                **item,

                "status": self.analytics.calculate_status(
                    item["kode"]
                )

            })

        return rows
