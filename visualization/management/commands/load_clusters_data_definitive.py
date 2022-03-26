import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import ClusterMatrixDefinitive
from django.template.defaultfilters import slugify
import pandas as pd
from tqdm import tqdm

class Command(BaseCommand):
    items = []


    def _get_smps(self):
        base = os.path.dirname(os.path.abspath('__file__'))
        full_path = "{}/visualization/management/commands/schistosoma_mansoni_genes_enriched_in_clusters_sep_v2.tsv".format(base)
        df = pd.read_csv(full_path, sep='\t')
        df = df.rename(columns={
            "transcripts_id": "transcripts_id",
            "Adjust.P.value": "adjusted_p_value",
            "Enrichment": "enrichment",
            "Description": "description",
            "Gene": "gene_id",
            "cluster": "cluster",
            "matrix_name": "matrix_name",
        	"gene_id": "gene_id",
            "gene_type": "gene_type"
        })
        df["matrix_name_slug"] = df["matrix_name"].apply(lambda x: slugify(x))
        df["cluster_slug"] = df["cluster"].apply(lambda x: slugify(x))
        for item in df.to_dict('records'):
            yield item

    def handle(self, *args, **options):
        if ClusterMatrixDefinitive.objects.count() > 0:
            return

        for cluster_item in tqdm(self._get_smps()):
            ClusterMatrixDefinitive.objects.get_or_create(**cluster_item)
