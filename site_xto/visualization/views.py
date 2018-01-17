from django.shortcuts import render, redirect, get_object_or_404
from visualization.tables import GeneLocationTable
from visualization.models import GeneLocation


def index(request):
    table = GeneLocationTable
    return render(request, "index.html", {'table': table})

def sm_view(request, gene_id):
    gene_obj = get_object_or_404(GeneLocation, gene_id = gene_id)

    context = {
            "LINC": gene_id,
            "GENE_OBJ": gene_obj,
            'URL_FIG_7A': "/static/Fig7A_S3/" + gene_id + ".png",
            "URL_FIG_6A": "/static/Fig6A/" + gene_id + ".png",
            "URL_FIG_S5": "/static/FigS5/" + gene_id + ".png",
    }
    return render(request, 'smlinc.html', context)