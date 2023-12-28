# bokeh version
from bokeh.plotting import figure
import random
import math


def export_graphs_hist(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        fruits = list(x.values())[0]["lables"]
        counts = list(x.values())[0]["counts"]
        p = figure(
            x_range=fruits,
            height=350,
            title=list(x.keys())[0],
            toolbar_location=None,
            tools="",
        )
        p.vbar(x=fruits, top=counts, width=0.9)
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        obj_lists.append(p)
    return "exported {}".format(str(len(chuncks))), obj_lists


def export_graphs_line(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        fruits = [x for x in range(len(list(x.values())[0]["lables"]))]
        counts = list(x.values())[0]["counts"]
        graph = figure(title=list(x.keys())[0])
        graph.line(fruits, counts, line_width=2)
        graph.xaxis.axis_label = ",".join(list(x.values())[0]["lables"])
        obj_lists.append(graph)
    return "exported {}".format(str(len(chuncks))), obj_lists


def export_graphs_pie_charts(chuncks):
    obj_lists = []
    for i, x in enumerate(chuncks):
        graph = figure(title=list(x.keys())[0])
        sectors = list(x.values())[0]["lables"]
        percentages = list(x.values())[0]["counts"]
        radians = [math.radians((percent / 100) * 360) for percent in percentages]
        start_angle = [math.radians(0)]
        prev = start_angle[0]
        for i in radians[:-1]:
            start_angle.append(i + prev)
        prev = i + prev
        end_angle = start_angle[1:] + [math.radians(0)]
        x = 0
        y = 0
        radius = 1
        color = [
            "#" + "".join([random.choice("0123456789ABCDEF") for j in range(6)])
            for i in range(len(sectors))
        ]
        for i in range(len(sectors)):
            graph.wedge(
                x,
                y,
                radius,
                start_angle=start_angle[i],
                end_angle=end_angle[i],
                color=color[i],
                legend_label=sectors[i],
            )
        obj_lists.append(graph)
    return obj_lists


def data_verience_whole_table(chuncks):
    newlist = [list(x.keys())[0] for x in chuncks]
    return {i: newlist.count(i) for i in newlist}
