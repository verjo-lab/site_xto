"""site_xto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from visualization.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('atlas/', atlas_index, name="atlas_index"),
    path('cluster-search/', lncrna_cluster_search, name="lncrna_cluster_search"),
    path('cluster-search/data/', SmLincExpressionDataFeed.as_view(), name="smlinc_data_feed"),
    path('sm_view/<gene_id>', sm_view, name="sm_view"),
    path('cluster/hes2', hes2_cluster, name="hes2_cluster"),
    path('cluster/<cluster>', cluster_view, name="cluster_view"),
    path('clusters/', clusters_view, name="clusters_view"),
    path('cluster_view/<matrix_name>', lncrnas_cluster_view, name="lncrnas_cluster_view"),
    path('cluster_view/enrichment/<matrix_name>', lncrnas_cluster_enrichment_view, name="lncrnas_cluster_enrichment_view"),
    path('smp_view/<gene_id>', smp_view, name="smp_view"),
    path('smp_search/', smp_search, name="smp_search"),
    path('cyto_view/', cyto_view, name="cyto_view"),
    path('net_downloads/', cytoscape_download, name="cytoscape_download"),
    path('datasets/', datasets_used, name="datasets_used"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
