import pandas as pd

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
            'URL_FIG_7A': "http://verjo101.butantan.gov.br/users/vinicius/static/Fig7A_S3/" + gene_id + ".png",
            "URL_FIG_6A": "http://verjo101.butantan.gov.br/users/vinicius/static/Fig6A/" + gene_id + ".png",
            "URL_FIG_S5": "http://verjo101.butantan.gov.br/users/vinicius/static/FigS5/" + gene_id + ".png",
    }
    columns_fcs = ["Gene ID", "Cerc", "3S", "24S", "Male", "Female"]
    columns_pccs = ["Compared Gene", "Gene", "Pearson Correlation Value", "p-value"]

    for i in ["Fig7A_S3", "Fig6A", "FigS5"]:
        for j in ["FCs", "PCCs"]:

            display_file = "http://verjo101.butantan.gov.br/users/vinicius/static/{folder}/{gene}-{cc}.tsv".format(
                folder=i,
                gene=gene_id,
                cc=j
            )
            context_name = "{i}_{j}_table".format(i=i, j=j)
            context_url_name = "URL_{i}_{j}_table".format(i=i, j=j)
            try:
                if j == "FCs":
                    columns = columns_fcs
                else:
                    columns = columns_pccs

                df =  pd.read_csv(
                    display_file,
                    sep = "\t",
                    header = None,
                    names = columns
                )

                context[context_name] = df.to_html(
                    classes = ["table", "table-striped", "table-hover"],
                    index = False,
                    border = 0
                )
                context[context_name].replace('border="1"', '')
                context[context_url_name] = display_file
                print(context_url_name)

            except:
                context[context_name] = ""
                context[context_url_name] = "#"


    return render(request, 'smlinc.html', context)

def cyto_view(request):
    return render(request, 'cytoscape.html')
