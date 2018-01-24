import json
from pprint import pprint

cyjs_path = json.load(open("/home/vinicius/GitHub/site_xto/site_xto/static/cytoscape/CoexpNetwork-cor0p8-DEedgeDE-lincSMP-181mainInt.cyjs"))

name_func = {}

for i in cyjs_path["elements"]["nodes"]:
    desc = [x for x in i["data"].keys() if x.startswith("description")]
    #name_func[i["data"]["name"]] = i["data"][desc[0]]
    # i["data"]["shared_name"] = i["data"][desc[0]]
    i["data"]["name"] = i["data"][desc[0]]


pprint(cyjs_path)