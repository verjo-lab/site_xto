from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from visualization.models import GeneLocation, ClusterMatrixDefinitive
from table import Table
from table.columns import Column, LinkColumn, Link
from table.tables import BaseTable, TableWidgets, TableMetaClass, TableData
from table.utils import A


import copy

class ModifiedTableWidgets(TableWidgets):
    def render_dom(self):
        dom = "<'row'" + self.search_box.dom + ">"
        dom += "rt"
        dom += "<'row'" + ''.join([self.info_label.dom, self.pagination.dom, self.length_menu.dom]) + ">"
        return mark_safe(dom)


class ModifiedBaseTable(BaseTable):
    def __init__(self, data=None):
        self.data = TableData(data, self)
        self.columns = copy.deepcopy(self.base_columns)
        self.addons = ModifiedTableWidgets(self)


ModifiedTable = TableMetaClass(str('ModifiedTable'), (ModifiedBaseTable,), {})

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


class SmLincExpression(ModifiedTable):
    matrix_name = LinkColumn(field='matrix_name', header="Gene ID", links=[Link(text=A('matrix_name'), viewname="lncrnas_cluster_view", kwargs={"matrix_name":A('matrix_name')})])
    transcripts_id = Column(field='transcripts_id', header="Transcript ID")
    gene_type = Column(field='gene_type', header="Gene Type")
    is_detected = Column(field='is_detected', header="Is Detected")
    description = Column(field='description', header="Description")

    class Meta:
        model = ClusterMatrixDefinitive
        ajax = True
        ajax_source = reverse_lazy('smlinc_data_feed')


from django.urls import reverse_lazy

class ClusterMatrixTable(ModifiedTable):
    matrix_name = LinkColumn(field='matrix_name', header="Matrix Name", links=[Link(text=A('matrix_name'), viewname="lncrnas_cluster_view", kwargs={"matrix_name": A('matrix_name')})])
    transcript_id = Column(field='transcripts_id', header="Transcript ID")
    gene = Column(field='gene_id', header="Gene")
    enrichment = Column(field='enrichment', header="Enrichment")
    adjusted_p_value = Column(field='adjusted_p_value', header="Adjusted P value")
    description = Column(field='description', header="Description")

    class Meta:
        model = ClusterMatrixDefinitive