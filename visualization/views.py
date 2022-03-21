import pandas as pd

from django.shortcuts import render, redirect, get_object_or_404

from visualization.tables import *
from visualization.models import *

from simple_search import search_filter
from table.views import FeedDataView


def index(request):
    table = GeneLocationTable
    return render(request, "index.html", {'table': table})


class SmLincExpressionDataFeed(FeedDataView):
    token = SmLincExpression.token

    def get_queryset(self):
        return super(SmLincExpressionDataFeed, self).get_queryset()


def lncrna_cluster_search(request):
    table = SmLincExpression
    return render(request, "schisto_cyte.html", {
        'table': table,
        'page_title': "Schistosoma mansoni Cyte Cluster"
    })

def lncrnas_cluster_view(request, matrix_name):
    cluster_smp_smlinc_obj = ClusterSMPSmlinc.objects.filter(matrix_name=matrix_name)

    return render(request, "smlinc_cluster.html", context={
        "page_title": "{} - Clusters".format(matrix_name),
        "SMP": matrix_name,
        "URL_FIG_ALL": "https://verjo101.butantan.gov.br/users/scRNA/teste/" + matrix_name + "_all.png",
        "URL_FIG_FEMALE": "https://verjo101.butantan.gov.br/users/scRNA/teste/" + matrix_name + "_female.png",
        "URL_FIG_IM": "https://verjo101.butantan.gov.br/users/scRNA/teste/" + matrix_name + "_IM.png",
        "URL_FIG_MALE": "https://verjo101.butantan.gov.br/users/scRNA/teste/" + matrix_name + "_male.png",
        "transcripts": cluster_smp_smlinc_obj
    })


def clusters_view(request):
    return render(request, 'clusters.html', {
        
    })



def cluster_view(request, cluster):
    table = ClusterMatrixTable(ClusterMatrix.objects.filter(cluster=cluster))
    return render(request, "schisto_cyte.html", {
        'table': table,
        'page_title': "{} Cluster Data".format(cluster)
    })


def datasets_used(request):
    return render(request, "datasets_used.html")

def cytoscape_download(request):
    return render(request, "cytoscape_download.html")

def sm_view(request, gene_id):
    gene_obj = get_object_or_404(GeneLocation, gene_id = gene_id)
    pd.set_option('display.max_colwidth', -1)
    context = {
            "LINC": gene_id,
            "GENE_OBJ": gene_obj,
            'URL_FIG_7A': "https://verjo101.butantan.gov.br/users/smLincDatabase/static/Fig7A_S3/" + gene_id + ".png",
            "URL_FIG_6A": "https://verjo101.butantan.gov.br/users/smLincDatabase/static/Fig6A/" + gene_id + ".png",
            "URL_FIG_S5": "https://verjo101.butantan.gov.br/users/smLincDatabase/static/FigS5/" + gene_id + ".png",
    }
    columns_fcs = ["Gene ID", "Cerc", "3S", "24S", "Male", "Female"]
    columns_pccs = ["Compared Gene", "Gene", "Pearson Correlation Value", "p-value", "B.-H. adjusted p-value"]

    for i in ["Fig7A_S3", "Fig6A", "FigS5"]:
        for j in ["FCs", "PCCs"]:
            if j == "PCCs":
                display_file = "http://verjolab.usp.br:8000/static/{folder}/{gene}-{cc}.tsv".format(
                    folder=i,
                    gene=gene_id,
                    cc=j + "-BHadj"
                )
            else:
                display_file = "http://verjolab.usp.br:8000/static/{folder}/{gene}-{cc}.tsv".format(
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
                    df["B.-H. adjusted p-value"] = df["B.-H. adjusted p-value"].apply(lambda x: '%.2e' % x)
                    df["p-value"] = df["p-value"].apply(lambda x: '%.2e' % x)

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
            'URL_FIG_7A': "http://verjolab.usp.br:8000/static/Fig7A_S3/" + gene_id + ".png",
            "URL_FIG_6A": "http://verjolab.usp.br:8000/static/Fig6A/" + gene_id + ".png",
            "URL_FIG_S5": "http://verjolab.usp.br:8000/static/FigS5/" + gene_id + ".png",
    }
    columns_fcs = ["Gene ID", "Cerc", "3S", "24S", "Male", "Female"]
    columns_pccs = ["Compared Gene", "Gene", "Pearson Correlation Value", "p-value", "B.-H. adjusted p-value"]

    for i in ["Fig7A_S3", "Fig6A", "FigS5"]:
        for j in ["FCs", "PCCs"]:

            if j == "PCCs":
                display_file = "http://verjolab.usp.br:8000/static/{folder}/{gene}-{cc}.tsv".format(
                    folder=i,
                    gene=gene_id,
                    cc=j + "-BHadj"
                )
            else:
                display_file = "http://verjolab.usp.br:8000/static/{folder}/{gene}-{cc}.tsv".format(
                    folder=i,
                    gene=gene_id,
                    cc=j
                )
            context_name = "{i}_{j}_table".format(i=i, j=j)
            context_url_name = "URL_{i}_{j}_table".format(i=i, j=j)
            try:
                if j == "FCs":
                    columns = columns_fcs
                    # df = df.sort_values('Female', ascending=True)
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

                    df["B.-H. adjusted p-value"] = df["B.-H. adjusted p-value"].apply(lambda x: '%.2e' % x)
                    df["p-value"] = df["p-value"].apply(lambda x: '%.2e' % x)


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
