import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404

from visualization.tables import GeneLocationTable
from visualization.models import GeneLocation, Smp

from simple_search import search_filter


def index(request):
    table = GeneLocationTable
    return render(request, "index.html", {'table': table})


def cytoscape_download(request):
    return render(request, "cytoscape_download.html")

def sm_view(request, gene_id):
    gene_obj = get_object_or_404(GeneLocation, gene_id = gene_id)
    pd.set_option('display.max_colwidth', -1)
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

                if j == "FCs":
                    df['Gene ID'] = df['Gene ID'].apply(
                        lambda x: '<a href="/smp_view/{0}">{0}</a>'.format(x) if "Smp" in x else '<a href="/sm_view/{0}">{0}</a>'.format(x)
                    )
                    df = df.sort_values('Female', ascending=True)
                else:
                    df['Compared Gene'] = df['Compared Gene'].apply(
                        lambda x: '<a href="/smp_view/{0}">{0}</a>'.format(x) if "Smp" in x else '<a href="/sm_view/{0}">{0}</a>'.format(x)
                    )

                context[context_name] = df.to_html(
                    classes = ["table", "table-striped", "table-hover"],
                    index = False,
                    border = 0,
                    escape=False
                )
                context[context_name].replace('border="1"', '')
                context[context_url_name] = display_file

            except:
                context[context_name] = ""
                context[context_url_name] = "#"

    return render(request, 'smlinc.html', context)

def smp_view(request, gene_id):
    pd.set_option('display.max_colwidth', -1)
    context = {
            "SMP": gene_id,
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

                if j == "FCs":
                    df['Gene ID'] = df['Gene ID'].apply(
                        lambda x: '<a href="/smp_view/{}">{}</a>'.format(x,x) if "Smp" in x else '<a href="/sm_view/{0}">{0}</a>'.format(x)
                    )
                else:
                    df['Gene'] = df['Gene'].apply(
                        lambda x: '<a href="/smp_view/{}">{}</a>'.format(x,x) if "Smp" in x else '<a href="/sm_view/{0}">{0}</a>'.format(x)
                    )

                context[context_name] = df.to_html(
                    classes = ["table", "table-striped", "table-hover"],
                    index = False,
                    border = 0,
                    escape=False
                )
                context[context_name].replace('border="1"', '')
                context[context_url_name] = display_file

            except:
                context[context_name] = ""
                context[context_url_name] = "#"

    return render(request, 'smpview.html', context)

def cyto_view(request):
    return render(request, 'cytoscape.html')

def smp_search(request):
    if request.method == "POST":
        smp = request.POST.get("smp")
        search_fields = ['^smp']
        f = search_filter(search_fields, smp)
        filtered = Smp.objects.filter(f)
        for item in filtered:
            print(dir(item))
            break
        return render(request, 'smp_search.html', {"qs": filtered, "s": smp})
    return redirect('/')
