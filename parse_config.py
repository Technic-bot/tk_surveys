from renames import col_remap
import graph_list

import pprint

# for orig, rem in renames.col_remap.items():
#    print(orig, rem)

survey = []
inv_map = {v: k for k, v in col_remap.items()}

for key, title in graph_list.pie_graphs:
    raw = inv_map[key]
    graph = { "raw": raw,
              "title": title,
              "name": key,
              "type": "pie"}  
    survey.append(graph)

for key, title, xaxis in graph_list.bar_num:
    raw = inv_map[key]
    graph = { "raw": raw,
              "title": title,
              "name": key,
              "type": "bar_num",
              "xaxis": xaxis}  
    survey.append(graph)

for key, title in graph_list.bar_cat:
    raw = inv_map[key]
    graph = { "raw": raw,
              "title": title,
              "name": key,
              "type": "bar_cat"}  
    survey.append(graph)

for key, title, yaxis in graph_list.histograms:
    raw = inv_map[key]
    graph = { "raw": raw,
              "title": title,
              "name": key,
              "yaxis": yaxis,
              "type": "histogram"}  
    survey.append(graph)

for key, title in graph_list.bar_order_keys:
    raw = inv_map[key]
    graph = { "raw": raw,
              "title": title,
              "name": key,
              "type": "bar_order_keys"}  
    survey.append(graph)

# pprint.pp(survey, indent=4)
with open("survey_config.py", "w") as f:
    f.write("survey = ")
    f.write(pprint.pformat(survey, indent=4))
    f.write("\n")
