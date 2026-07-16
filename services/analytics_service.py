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
            df["kode"] == kode
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
    def _safe_divide(numerator, denominator):

        if denominator == 0:
            return 0.0

        return float(round(
            numerator / denominator * 100,
            2
        ))
    
    def _build_status(
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

    # ==============================================================================
    # PUBLIC
    # ==============================================================================
    
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

            "kinerja": self.get_kinerja(kode),

            "anggaran": self.get_anggaran(kode),

            "timeline": self.get_timeline(kode),

            "hambatan": self.get_hambatan(kode),

            "rekomendasi": self.get_rekomendasi(kode)

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

    def get_kinerja(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return None

        return {

            "target": int(
                row["target_kinerja"]
            ),

            "realisasi": float(
                row["realisasi_kinerja"]
            ),

            "satuan": str(
                row["satuan"]
            )

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

                "status": self._build_status(
                    value=0,
                    target=0,
                    realisasi=0
                )

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

            "status": self._build_status(

                value=persentase,

                target=total_target,

                realisasi=total_realisasi

            )

        }
    
    def get_timeline(self, kode):

        return {

            "tw1": None,

            "tw2": None,

            "tw3": None,

            "tw4": None

        }
    
    def get_hambatan(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return ""

        value = str(
            row["FAKTOR PENGHAMBAT"]
        ).strip()

        if value in ("", "0", "nan", "None"):
            return None

        return value
    
    def get_rekomendasi(self, kode):

        row = self._row(
            self.realisasi,
            kode
        )

        if row is None:
            return ""

        value = str(
            row["REKOMENDASI"]
        ).strip()

        if value in ("", "0", "nan", "None"):
            return None

        return value
