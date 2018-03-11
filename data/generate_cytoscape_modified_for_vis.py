import json

list_sergio = [
    "integral to membrane",
    "intrinsic to membrane",
    "extracellular region",
    "extracellular region part",
    "membrane part",
    "membrane",
    "extracellular space",
    "DNA integration",
    "RNA-directed DNA polymerase activity",
    "proteinaceous extracellular matrix",
    "RNA-dependent DNA replication",
    "extracellular matrix",
    "dynein complex",
    "monovalent inorganic cation transmembrane transporter",
    "G-protein coupled receptor protein signaling pathway",
    "G-protein coupled receptor activity",
]

with open("PATH_HERE/static/cytoscape/CoexpNetwork-cor0p8-DEedgeDE-lincSMP-181mainInt_v2.cyjs", "r") as js:
    a = json.load(js)

    for item in a["elements"]["nodes"]:
        if item["data"]["name"] in list_sergio:
            item["data"]["pValue_GO_DE_2359SMPs_cor0p8_181lincRNAs"] = 1.000000
            # print(item["data"])
        else:
            item["data"]["pValue_GO_DE_2359SMPs_cor0p8_181lincRNAs"] = 0.000000

with open("PATH_HERE/static/cytoscapenew_cyto2.cyjs", 'w') as b:
    json.dump(a, b)
