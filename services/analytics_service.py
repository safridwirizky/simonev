from datetime import date, datetime
import pandas as pd


class AnalyticsService:

    TRIWULAN_MAP = {
        1: [1],
        2: [1, 2],
        3: [1, 2, 3],
        4: [1, 2, 3, 4],
    }

    def __init__(
        self,
        realisasi_df,
        anggaran_df,
        settings
    ):

        self.realisasi = realisasi_df
        self.anggaran = anggaran_df

        self.settings = settings
    
    # ==============================================================================
    # PRIVATE : DATA
    # ==============================================================================
    
    def _row(self, df, kode):

        row = df.loc[
            df["kode"] == str(kode)
        ]

        if row.empty:
            return None

        return row.iloc[0]
    
    def _period_columns(self, prefix):

        return [
            f"{prefix}_tw{i}"
            for i in self.TRIWULAN_MAP[self.settings.triwulan]
        ]
    
    # ==============================================================================
    # PRIVATE : FORMATTER
    # ==============================================================================

    @staticmethod
    def _currency(value):

        value = float(value)

        return f"Rp {value:,.0f}".replace(",", ".")
    
    @staticmethod
    def _number(value):

        return f"{value:,.0f}".replace(",", ".")

    @staticmethod
    def _safe_divide(numerator, denominator):

        if denominator == 0:
            return 0.0

        return float(round(
            numerator / denominator * 100,
            2
        ))
    
    def _build_anggaran_status(
        self,
        value: float,
        target: float,
        realisasi: float
    ):

        if value >= 80:
            label = "Baik"
            color = "bg-success"
            icon = "bi-check-circle-fill"

        elif value >= 60:
            label = "Perlu Perhatian"
            color = "bg-warning"
            icon = "bi-exclamation-triangle-fill"

        else:
            label = "Kritis"
            color = "bg-danger"
            icon = "bi-x-circle-fill"

        return {
            "value": value,                       # untuk width progress bar
            "display": f"{round(value):.0f}%",    # tampil di tabel
            "exact": f"{value:.2f}%",             # tooltip / detail

            "target": {
                "value": target,
                "display": self._currency(target)
            },

            "realisasi": {
                "value": realisasi,
                "display": self._currency(realisasi)
            },

            "label": label,
            "color": color,
            "icon": icon,
        }
    
    def _build_anggaran_chart(
        self,
        realisasi,
        target
    ):

        periods = [
            ("TW I", "target_tw1", "realisasi_tw1"),
            ("TW II", "target_tw2", "realisasi_tw2"),
            ("TW III", "target_tw3", "realisasi_tw3"),
            ("TW IV", "target_tw4", "realisasi_tw4"),
        ]

        triwulan = []

        for periode, target_col, realisasi_col in periods:

            if realisasi is None or target is None:

                target_value = 0
                realisasi_value = 0

            else:

                target_value = float(target[target_col])
                realisasi_value = float(realisasi[realisasi_col])

            triwulan.append({

                "periode": periode,

                "target": {
                    "value": target_value,
                    "display": self._currency(target_value)
                },

                "realisasi": {
                    "value": realisasi_value,
                    "display": self._currency(realisasi_value)
                }

            })

        return {
            "triwulan": triwulan
        }
    
    def _build_metric(
        self,
        value,
        formatter=None
    ):
        """
        Build metric payload.

        Returns:
            {
                "value": 100,
                "display": "100"
            }
        """

        return {
            "value": value,
            "display": (
                formatter(value)
                if formatter
                else str(value)
            )
        }
    
    def _build_kinerja(
        self,
        target,
        realisasi,
        satuan
    ):

        persentase = self._safe_divide(
            realisasi,
            target
        )

        return {

            "target": self._build_metric(
                target,
                self._number
            ),

            "realisasi": self._build_metric(
                realisasi,
                self._number
            ),

            "persentase": persentase,

            "satuan": satuan

        }
    
    def _clean_text(self, value):

        if value is None:
            return None

        value = str(value).strip()

        if value.lower() in {
            "",
            "0",
            "0.0",
            "nan",
            "none"
        }:
            return None

        return value
    
    def _clean_date(self, value):
        if value is None:
            return None

        if pd.isna(value):
            return None

        if isinstance(value, (datetime, date)):
            return value.strftime("%d %B %Y")

        value = str(value).strip()

        if value.lower() in {
            "",
            "0",
            "0.0",
            "nan",
            "none"
        }:
            return None

        try:
            return pd.to_datetime(value).strftime("%d %B %Y")
        except Exception:
            return value

    # ==============================================================================
    # PUBLIC
    # ==============================================================================
    
    def get_summary(self):

        total_sub_kegiatan = len(self.realisasi)

        total_anggaran = self.anggaran[
            "PAGU"
        ].fillna(0).sum()

        total_realisasi = self.realisasi[
            "REALISASI"
        ].fillna(0).sum()

        persentase = 0

        if total_anggaran > 0:

            persentase = (
                total_realisasi /
                total_anggaran
            ) * 100

        return {

            "total_sub_kegiatan": total_sub_kegiatan,

            "total_anggaran": total_anggaran,

            "total_realisasi": total_realisasi,

            "persentase_realisasi": round(
                persentase,
                2
            )

        }
    
    def get_sub_kegiatan(self):

        return (

            self.realisasi[
                [
                    "kode",

                    "bidang",

                    "sub_kegiatan"
                ]
            ]

            .sort_values(
                by=[
                    "bidang",
                    "sub_kegiatan"
                ]
            )

            .to_dict(
                orient="records"
            )

        )

    def get_detail(self, kode):

        return {

            "header": self.get_header(kode),

            "anggaran": self.get_anggaran(kode),

            "kinerja": self.get_kinerja(kode),

            "evaluasi": self.get_evaluasi(kode),

            "tindak_lanjut": self.get_tindak_lanjut(kode)

        }

    def get_header(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return None

        return {

            "kode": str(row["kode"]),

            "bidang": str(row["bidang"]),

            "sub_kegiatan": str(row["sub_kegiatan"])

        }

    def get_anggaran(self, kode):

        realisasi = self._row(
            self.realisasi,
            kode
        )

        target = self._row(
            self.anggaran,
            kode
        )

        chart = self._build_anggaran_chart(
            realisasi,
            target
        )

        if realisasi is None or target is None:

            return {

                "target": {
                    "value": 0,
                    "display": self._currency(0)
                },

                "realisasi": {
                    "value": 0,
                    "display": self._currency(0)
                },

                "status": self._build_anggaran_status(
                    value=0,
                    target=0,
                    realisasi=0
                ),

                "chart": chart

            }

        total_realisasi = realisasi[
            self._period_columns("realisasi")
        ].sum()

        total_target = target[
            self._period_columns("target")
        ].sum()

        persentase = self._safe_divide(
            total_realisasi,
            total_target
        )

        return {

            "target": {

                "value": total_target,

                "display": self._currency(
                    total_target
                )

            },

            "realisasi": {

                "value": total_realisasi,

                "display": self._currency(
                    total_realisasi
                )

            },

            "status": self._build_anggaran_status(

                value=persentase,

                target=total_target,

                realisasi=total_realisasi

            ),

            "chart": chart

        }

    def get_kinerja(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return None

        return self._build_kinerja(

            target=float(
                row["target_kinerja"]
            ),

            realisasi=float(
                row["realisasi_kinerja"]
            ),

            satuan=str(
                row["satuan"]
            )

        )
    
    def get_anggaran_chart(self, kode):

        realisasi = self._row(
            self.realisasi,
            kode
        )

        target = self._row(
            self.anggaran,
            kode
        )

        if realisasi is None or target is None:

            return {

                "categories": [
                    "TW I",
                    "TW II",
                    "TW III",
                    "TW IV"
                ],

                "target": [
                    0,
                    0,
                    0,
                    0
                ],

                "realisasi": [
                    0,
                    0,
                    0,
                    0
                ]

            }

        return {

            "categories": [
                "TW I",
                "TW II",
                "TW III",
                "TW IV"
            ],

            "target": [

                float(target["target_tw1"]),

                float(target["target_tw2"]),

                float(target["target_tw3"]),

                float(target["target_tw4"])

            ],

            "realisasi": [

                float(realisasi["realisasi_tw1"]),

                float(realisasi["realisasi_tw2"]),

                float(realisasi["realisasi_tw3"]),

                float(realisasi["realisasi_tw4"])

            ]

        }
    
    def get_evaluasi(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return None

        hambatan = self._clean_text(
            row["FAKTOR PENGHAMBAT"]
        )

        rekomendasi = self._clean_text(
            row["REKOMENDASI"]
        )

        if hambatan is None and rekomendasi is None:
            return None

        return {

            "hambatan": hambatan,

            "rekomendasi": rekomendasi

        }
    
    def get_tindak_lanjut(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return None

        status = self._clean_text(
            row["STATUS TINDAK LANJUT"]
        )

        tanggal = self._clean_date(
            row["Tanggal Tindak Lanjut"]
        )

        catatan = self._clean_text(
            row["Catatan Tindak Lanjut"]
        )

        if status is None and tanggal is None and catatan is None:
            return None

        badge = {

            "Belum Ditindaklanjuti": "bg-secondary",

            "Diproses": "bg-warning text-dark",

            "Selesai": "bg-success"

        }.get(status, "bg-secondary")

        return {

            "status": status,

            "badge": badge,

            "tanggal": tanggal,

            "catatan": catatan

        }
