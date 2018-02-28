import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import GeneLocation
import pandas as pd
from tqdm import tqdm


class Command(BaseCommand):
    @staticmethod
    def _get_genomic_locs():
        base = os.path.dirname(os.path.abspath('__file__'))
        full_path = "{}/visualization/management/commands/s2_table_genomic_loc_of_lncrnas.xlsx".format(base)
        gen_locs = []
        df = pd.read_excel(full_path)
        print("Pré-processamento dos dados")
        for df_i in tqdm(df.to_dict('records')):
            gen_locs.append({
                "chromosome": df_i["chrom"].replace("_", " "),
                "chromosome_start": df_i["chomStart"],
                "chromosome_end": df_i["chromEnd"],
                "strand": df_i["strand"],
                "gene_id": df_i["geneID"],
                "block_counts": df_i["blockCount"],
                "block_sizes": df_i["blockSizes"],
                "block_starts": df_i["blockStarts"],
                "link": "http://schistosoma.usp.br/cgi-bin/hgTracks?hgS_doOtherUser=submit&hgS_otherUserName=localadmin&hgS_otherUserSessionName=PLOSPathogensSubmitted&position=" + str(df_i["chrom"]) + ":" + str(df_i["chomStart"]) + "-" + str(df_i["chromEnd"])
            })
        return gen_locs


    def handle(self, *args, **options):
        gen_locs = self._get_genomic_locs()
        print("Inserção no banco")
        for gen_loc in tqdm(gen_locs):
            try:
                gen_loc_obj = GeneLocation.objects.create(**gen_loc)
            except IntegrityError as e:
                print(
                    "Gene ID '{}' already exists in the database".format(
                        gen_loc_obj.gene_id
                    )
                )