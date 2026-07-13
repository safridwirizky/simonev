class AnalyticsService:

    TRIWULAN = {
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
    # PRIVATE
    # ==============================================================================
    
    def _build_status(self, persentase):

        if persentase >= 80:
            return {
                "persentase": persentase,
                "kategori": "success",
                "label": "Baik",
                "icon": "bi-check-circle-fill",
                "color": "bg-success"
            }

        elif persentase >= 60:
            return {
                "persentase": persentase,
                "kategori": "warning",
                "label": "Perlu Perhatian",
                "icon": "bi-exclamation-triangle-fill",
                "color": "bg-warning"
            }

        return {
            "persentase": persentase,
            "kategori": "danger",
            "label": "Kritis",
            "icon": "bi-x-circle-fill",
            "color": "bg-danger"
        }
    
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

            for i in self.TRIWULAN[
                self.settings.triwulan
            ]

        ]
    
    @staticmethod
    def _safe_divide(numerator, denominator):

        if denominator == 0:
            return 0.0

        return float(round(
            numerator / denominator * 100,
            2
        ))

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

                "bidang"

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

        return {

            "kode": row["kode"],

            "bidang": row["bidang"],

            "sub_kegiatan": row["sub_kegiatan"],

            "target_kinerja": row["target_kinerja"],

            "satuan": row["satuan"]

        }

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
            return self._build_status(0)

        realisasi_columns = self._period_columns(
            "realisasi"
        )

        target_columns = self._period_columns(
            "target"
        )

        total_realisasi = realisasi[
            realisasi_columns
        ].sum(skipna=True)

        total_target = target[
            target_columns
        ].sum()

        persen = self._safe_divide(
            total_realisasi,
            total_target
        )

        return self._build_status(persen)
