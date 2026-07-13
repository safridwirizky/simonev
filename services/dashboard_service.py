def table(self):

    rows = []

    for item in self.analytics.get_sub_kegiatan():

        rows.append({

            **item,

            "status":

            self.analytics.calculate_status(

                item["kode"]

            )

        })

    return rows
