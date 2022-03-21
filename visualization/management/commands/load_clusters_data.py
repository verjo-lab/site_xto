import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import Smp, ClusterMatrix
import pandas as pd
from tqdm import tqdm


# Code used to generate this smp - smlinc listing

# import pandas as pd
# content = pd.read_csv("schistosoma_mansoni_genes_enriched_in_clusters.tsv", sep="\t")
# content["transcripts_ids"] = content["transcripts_ids"].apply(lambda x: x.split(","))
# content = content.explode(["transcripts_ids"])
# content.to_csv("schistosoma_mansoni_genes_enriched_in_clusters_sep.tsv", sep="\t", index=False)

class Command(BaseCommand):
    items = []


    def _get_smps(self):
        base = os.path.dirname(os.path.abspath('__file__'))
        full_path = "{}/visualization/management/commands/schistosoma_mansoni_genes_enriched_in_clusters_sep.tsv".format(base)
        df = pd.read_csv(full_path, sep='\t')
        df["transcripts_ids"] = df["transcripts_ids"].apply(lambda x: Smp.objects.get_or_create(smp=x)[0])
        df = df.rename(columns={
            "transcripts_ids": "transcript_id",
            "Adjust P-value": "adjusted_p_value",
            "Enrichment": "enrichment",
            "Description": "description",
            "Gene": "gene"
        })
        df["cluster"] = df["cluster"].apply(lambda x: x.replace(" ", "-"))
        for item in df.to_dict('records'):
            yield item

    def handle(self, *args, **options):
        if ClusterMatrix.objects.count() > 0:
            return

        for cluster_item in tqdm(self._get_smps()):
            ClusterMatrix.objects.get_or_create(**cluster_item)