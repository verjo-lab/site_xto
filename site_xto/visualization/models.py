from django.db import models

class GeneLocation(models.Model):
    chromosome = models.CharField(default="", max_length=256)
    gene_id = models.CharField(default="", max_length=256)
    chromosome_start = models.IntegerField()
    chromosome_end = models.IntegerField()
    strand = models.CharField(default="", max_length=256)
    block_counts = models.IntegerField()
    block_sizes = models.CharField(default="", max_length=256)
    block_starts = models.CharField(default="", max_length=256)
    link = models.URLField()