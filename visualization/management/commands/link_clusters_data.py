import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import Smp, ClusterMatrix, ClusterSMPSmlinc
import pandas as pd
from tqdm import tqdm

class Command(BaseCommand):
    def handle(self, *args, **options):
        for cluster_smp_smlinc in ClusterSMPSmlinc.objects.all():
            cluster_matrix_obj = ClusterMatrix.objects.filter(
                gene=cluster_smp_smlinc.gene_id.smp,
                matrix_name=cluster_smp_smlinc.matrix_name,
                transcript_id__smp=cluster_smp_smlinc.transcripts_id
            ).first()
            cluster_smp_smlinc.cluster_matrix = cluster_matrix_obj
            try:
                cluster_smp_smlinc.description = cluster_matrix_obj.description
            except:
                pass
            cluster_smp_smlinc.save()