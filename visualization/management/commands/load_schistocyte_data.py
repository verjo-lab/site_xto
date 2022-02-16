import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import Smp, ClusterSMPSmlinc
import pandas as pd
from tqdm import tqdm


# Code used to generate this smp - smlinc listing

# import pandas as pd
# content = pd.read_csv("schisto_genes.tsv", sep="\t")
# content["transcripts_id"] = content["transcripts_id"].apply(lambda x: x.split(","))
# content = content.explode(["transcripts_id"])
# content.to_csv("smps_smlincs.tsv", sep="\t")
# content.to_csv("smps_smlincs.tsv", sep="\t", index=False)


class Command(BaseCommand):
    def _get_smps(self):
        base = os.path.dirname(os.path.abspath('__file__'))
        full_path = "{}/visualization/management/commands/smps_smlincs.tsv".format(base)
        df = pd.read_csv(full_path, sep='\t')
        df["gene_id"] = df["gene_id"].apply(lambda x: Smp.objects.get_or_create(smp=x)[0])
        for item in df.to_dict('records'):
            yield item

    def handle(self, *args, **options):
        for cluster_item in tqdm(self._get_smps()):
            ClusterSMPSmlinc.objects.get_or_create(**cluster_item)