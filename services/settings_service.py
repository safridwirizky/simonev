import json
from pathlib import Path


class SettingsService:
    """
    Global application settings.

    Saat ini hanya menyimpan:
    - Tahun Evaluasi
    - Triwulan Evaluasi
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        self.reload()

    def reload(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            self._settings = json.load(f)

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(
                self._settings,
                f,
                indent=4,
                ensure_ascii=False
            )

    @property
    def tahun(self):
        return self._settings["tahun"]

    @property
    def triwulan(self):
        return self._settings["triwulan"]

    def set_period(self, tahun: int, triwulan: int):
        self._settings["tahun"] = tahun
        self._settings["triwulan"] = triwulan
        self.save()
