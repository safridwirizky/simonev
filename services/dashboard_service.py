from services.analytics_service import AnalyticsService


class DashboardService:

    def __init__(self, excel_service, settings_service):

        self.excel = excel_service
        self.settings = settings_service

        self.analytics = AnalyticsService(
            self.excel.realisasi,
            self.excel.anggaran,
            self.settings
        )

    def table(self):
        """
        Data untuk halaman monitoring.
        Sementara masih dummy.
        """

        return [
            {
                "kode": "5.01.02.2.16",
                "bidang": "PPEPD",
                "sub_kegiatan": "Penyusunan RKPD",
                "status": 82.5
            },
            {
                "kode": "5.01.02.2.17",
                "bidang": "Litbang",
                "sub_kegiatan": "Kajian Strategis",
                "status": 63.4
            }
        ]

    def detail(self, kode):
        """
        Data dashboard sub kegiatan.
        Sementara masih dummy.
        """

        return {
            "identitas": {
                "kode": kode,
                "bidang": "",
                "sub_kegiatan": ""
            },
            "kinerja": {},
            "anggaran": {},
            "timeline": []
        }
