import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from visualization.models import GeneLocation, Smp
import pandas as pd
from tqdm import tqdm


class Command(BaseCommand):
    @staticmethod
    def _get_smps():
        base = os.path.dirname(os.path.abspath('__file__'))
        full_path = "{}/visualization/management/commands/smps.txt".format(base)
        smps = []
        print("Pré-processamento das SMPs")
        f = open(full_path)
        for line in tqdm(f):
            smps.append({
                "smp": line.strip(),
            })
        return smps


    def handle(self, *args, **options):
        if Smp.objects.count() > 0:
            return
            
        smps = self._get_smps()
        print("Inserção no banco")
        for smp in tqdm(smps):
            try:
                smp = Smp.objects.create(**smp)
            except IntegrityError as e:
                print(
                    "Smp '{}' already exists in the database".format(
                        smp.smp
                    )
                )
