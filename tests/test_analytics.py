from config import Config

from services.excel_service import ExcelService
from services.settings_service import SettingsService
from services.analytics_service import AnalyticsService

excel = ExcelService()
excel.load(Config.EXCEL_FILE)

settings = SettingsService(Config.SETTINGS_FILE)

analytics = AnalyticsService(
    excel.realisasi,
    excel.anggaran,
    settings
)

print(excel.realisasi.columns.tolist())

print(excel.realisasi.head())

print("=" * 50)

print("DAFTAR SUB KEGIATAN")

print("=" * 50)

print(analytics.get_sub_kegiatan())

print()

kode = "5.01.01"

print("=" * 50)

print(f"STATUS : {kode}")

print("=" * 50)

print( analytics.calculate_status(kode) )
