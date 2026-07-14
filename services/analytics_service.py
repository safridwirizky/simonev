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

        row = self._row(

            self.realisasi,

            kode

        )

        if row is None:

            return None

        return dict(
            kode=row["kode"],
            bidang=row["bidang"],
            sub_kegiatan=row["sub_kegiatan"],
            target_kinerja=row["target_kinerja"],
            satuan=row["satuan"]
        )

    def calculate_status(self, kode):

        realisasi = self._row(
            self.realisasi,
            kode
        )

        target = self._row(
            self.anggaran,
            kode
        )

        if realisasi is None or target is None:
            return self._build_status(
                value=0,
                target=0,
                realisasi=0
            )

        realisasi_columns = self._period_columns(
            "realisasi"
        )

        target_columns = self._period_columns(
            "target"
        )

        total_realisasi = realisasi[
            realisasi_columns
        ].sum()

        total_target = target[
            target_columns
        ].sum()

        persentase = self._safe_divide(
            total_realisasi,
            total_target
        )

        return self._build_status(
            value=persentase,
            target=total_target,
            realisasi=total_realisasi
        )
