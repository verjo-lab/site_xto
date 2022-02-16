# install.packages(c("Seurat4", "patchwork", "tidyverse", "magrittr", "glue"))
library(Seurat)
library(patchwork)
library(tidyverse)
library(magrittr)
library(glue)

# Loading data

so = readRDS("sm_all_genes_seurat.rds")
cell_ids = so$orig.ident %>%
            enframe(name = "cell_id",value = "sample") %>%
            mutate(sex = str_match(sample,"(.*)?[[:digit:]]")[,2])

embeddings = so@reductions$ref.umap@cell.embeddings %>% as_tibble(rownames = "cell_id")
clusters = so$predicted.id %>% enframe(name = "cell_id",value = "ref_cluster")
cell_ids = Reduce(inner_join,list(cell_ids,embeddings,clusters))

m = so@assays$SCT@counts

all_genes = rownames(m)

gene_plot = function(gene_name = NULL){
          gene = str_replace_all(gene_name,"_","-")

          exp = m[gene,] %>% enframe(name = "cell_id",value = "exp")

          exp = cell_ids %>% inner_join(exp) %>% mutate(exp = exp/max(exp)*100)


          # Making plots

          all_g = exp %>%
            ggplot(aes(refUMAP_1,refUMAP_2)) +
            geom_point(aes(colour = exp),size = 0.2) +
            theme_classic() +
            scale_colour_gradientn(colours = c("grey","blue","purple","yellow","red"),
                                   name = "Expression %") +
            xlab("UMAP 1") + ylab("UMAP 2") +
            ggtitle(glue("{gene} - All cells"))

          im_g = exp %>%
            filter(sex == "IM") %>%
            ggplot(aes(refUMAP_1,refUMAP_2)) +
            geom_point(aes(colour = exp),size = 0.2) +
            theme_classic() +
            scale_colour_gradientn(colours = c("grey","blue","purple","yellow","red"),
                                   name = "Expression %") +
            xlab("UMAP 1") + ylab("UMAP 2") +
            ggtitle(glue("{gene} - Immature Female"))

          mal_g = exp %>%
            filter(sex == "Male") %>%
            ggplot(aes(refUMAP_1,refUMAP_2)) +
            geom_point(aes(colour = exp),size = 0.2) +
            theme_classic() +
            scale_colour_gradientn(colours = c("grey","blue","purple","yellow","red"),
                                   name = "Expression %") +
            xlab("UMAP 1") + ylab("UMAP 2") +
            ggtitle(glue("{gene} - Male"))

          fem_g = exp %>%
            filter(sex == "Female") %>%
            ggplot(aes(refUMAP_1,refUMAP_2)) +
            geom_point(aes(colour = exp),size = 0.2) +
            theme_classic() +
            scale_colour_gradientn(colours = c("grey","blue","purple","yellow","red"),
                                   name = "Expression %") +
            xlab("UMAP 1") + ylab("UMAP 2") +
            ggtitle(glue("{gene} - Female"))

          # Saving the image

          ggsave(glue("{gene}_all.png"),all_g,width = 6,height = 6)
          ggsave(glue("{gene}_IM.png"),im_g,width = 6,height = 6)
          ggsave(glue("{gene}_male.png"),mal_g,width = 6,height = 6)
          ggsave(glue("{gene}_female.png"),fem_g,width = 6,height = 6)

  }

lapply(all_genes, gene_plot)