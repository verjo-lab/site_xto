from visualization.models import GeneLocation
from table import Table
from table.columns import Column, LinkColumn, Link

from table.utils import A


class GeneLocationTable(Table):
    gene_id = LinkColumn(field='gene_id', header="Gene ID", links=[Link(text=A('gene_id'), viewname="sm_view", kwargs={"gene_id":A('gene_id')})])
    chromosome = Column(field='chromosome', header="Chromosome")
    chromosome_start = Column(field='chromosome_start', header="Chromosome Start")
    chromosome_end = Column(field='chromosome_end', header="Chromosome End")
    strand = Column(field='strand', header="Strand")
    block_counts = Column(field='block_counts', header="Block Count")
    class Meta:
        model = GeneLocation
        search_placeholder = "Search for your gene"
