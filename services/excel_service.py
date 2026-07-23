from pathlib import Path

import pandas as pd

from constants import (
    REALISASI_REQUIRED_COLUMNS,
    ANGGARAN_REQUIRED_COLUMNS,
    REALISASI_RENAME,
    ANGGARAN_RENAME,
)


class ExcelService:

    def __init__(self):
        self._realisasi = pd.DataFrame()
        self._anggaran = pd.DataFrame()

    def load(self, file_path):

        file_path = Path(file_path)

        if not file_path.exists():
            raise FileNotFoundError(
                f"File Excel tidak ditemukan:\n{file_path}"
            )

        workbook = pd.ExcelFile(file_path)

        self._validate_sheet(workbook)

        realisasi = pd.read_excel(
            workbook,
            sheet_name="REALISASI"
        )

        anggaran = pd.read_excel(
            workbook,
            sheet_name="ANGGARAN_KAS"
        )

        self._validate_columns(
            realisasi,
            REALISASI_REQUIRED_COLUMNS,
            "REALISASI"
        )

        self._validate_columns(
            anggaran,
            ANGGARAN_REQUIRED_COLUMNS,
            "ANGGARAN_KAS"
        )

        self._realisasi = self._normalize(
            realisasi,
            REALISASI_RENAME
        )

        self._anggaran = self._normalize(
            anggaran,
            ANGGARAN_RENAME
        )

    def reload(self, file_path):
        self.load(file_path)

    @property
    def realisasi(self):
        return self._realisasi.copy()

    @property
    def anggaran(self):
        return self._anggaran.copy()

    # ==========================
    # PRIVATE
    # ==========================

    def _validate_sheet(self, workbook):

        required = {
            "REALISASI",
            "ANGGARAN_KAS"
        }

        available = set(workbook.sheet_names)

        missing = required - available

        if missing:
            raise ValueError(
                f"Sheet tidak ditemukan: {', '.join(missing)}"
            )

    def _validate_columns(
        self,
        df,
        required_columns,
        sheet_name
    ):

        missing = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing:
            raise ValueError(
                f"Sheet '{sheet_name}' kehilangan kolom:\n"
                + "\n".join(missing)
            )

    def _normalize(
        self,
        df,
        rename_map
    ):

        df = df.rename(columns=rename_map)

        df.columns = (
            df.columns
            .str.strip()
        )

        object_columns = df.select_dtypes(
            include="object"
        ).columns

        numeric_columns = df.select_dtypes(
            exclude="object"
        ).columns

        df[object_columns] = df[object_columns].fillna("")

        df[numeric_columns] = df[numeric_columns].fillna(0)

        # Normalisasi kolom kode
        if "kode" in df.columns:
            df["kode"] = (
                df["kode"]
                .astype(str)
                .str.strip()
            )

        return df
    
    @property
    def total_sub_kegiatan(self):
        return len(self._realisasi)
