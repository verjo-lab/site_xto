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

class Smp(models.Model):
    smp =  models.CharField(default="", max_length=256)

    def __repr__(self):
        return self.smp

    def __str__(self):
        return self.smp


class ClusterSMPSmlinc(models.Model):
    gene_id = models.ForeignKey("Smp", on_delete=models.CASCADE)
    matrix_name = models.CharField(max_length=2000, default="", blank=True)
    transcripts_id = models.CharField(max_length=2000, default="", blank=True)
    gene_type = models.CharField(max_length=2000, default="", blank=True)
    is_detected = models.BooleanField(default = False)
