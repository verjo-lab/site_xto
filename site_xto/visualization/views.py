from django.shortcuts import render, redirect, get_object_or_404
from visualization.tables import GeneLocationTable
from visualization.models import GeneLocation


def index(request):
    table = GeneLocationTable
    return render(request, "index.html", {'table': table})

def sm_view(request, gene_id):
    gene_obj = get_object_or_404(GeneLocation, gene_id = gene_id)
    return redirect(gene_obj.link)