class AnalyticsService:

    def __init__(self, realisasi_df, anggaran_df, settings):

        self.realisasi = realisasi_df
        self.anggaran = anggaran_df
        self.settings = settings
