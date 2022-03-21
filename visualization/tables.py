from django.urls import reverse_lazy

from visualization.models import GeneLocation, ClusterSMPSmlinc, ClusterMatrix
from table import Table
from table.columns import Column, LinkColumn, Link

from table.utils import A


class GeneLocationTable(Table):
    gene_id = LinkColumn(field='gene_id', header="SmLINC", links=[Link(text=A('gene_id'), viewname="sm_view", kwargs={"gene_id":A('gene_id')})])
    chromosome = Column(field='chromosome', header="Chromosome")
    chromosome_start = Column(field='chromosome_start', header="Chromosome Start")
    chromosome_end = Column(field='chromosome_end', header="Chromosome End")
    strand = Column(field='strand', header="Strand")
    block_counts = Column(field='block_counts', header="# of Exons")
    class Meta:
        model = GeneLocation
        search_placeholder = "Search for your SmLINC"


class SmLincExpression(Table):
    matrix_name = LinkColumn(field='matrix_name', header="Gene ID", links=[Link(text=A('matrix_name'), viewname="lncrnas_cluster_view", kwargs={"matrix_name":A('matrix_name')})])
    transcripts_id = Column(field='transcripts_id', header="Transcript ID")
    gene_type = Column(field='gene_type', header="Gene Type")
    is_detected = Column(field='is_detected', header="Is Detected")

    class Meta:
        model = ClusterSMPSmlinc
        ajax = True
        ajax_source = reverse_lazy('smlinc_data_feed')


from django.urls import reverse_lazy

class ClusterMatrixTable(Table):
    matrix_name = LinkColumn(field='matrix_name', header="Matrix Name", links=[Link(text=A('matrix_name'), viewname="lncrnas_cluster_view", kwargs={"matrix_name": A('matrix_name')})])
    transcript_id = Column(field='transcript_id', header="Transcript ID")
    gene = Column(field='gene', header="Gene")
    enrichment = Column(field='enrichment', header="Enrichment")
    adjusted_p_value = Column(field='adjusted_p_value', header="Adjusted P value")
    description = Column(field='description', header="Description")

    class Meta:
        model = ClusterMatrix