import svgwrite
from topo import undirected
from geom import point_on_seg


def plot_pattern(file_path, uv_coords, cut_ratios, connected, match, scale=100):
    draw = svgwrite.Drawing(file_path, ("{}mm".format(scale), "{}mm".format(scale)), profile="tiny")
    draw.viewbox(0, 0, 1, 1)
    pat_g = draw.g(stroke=svgwrite.rgb(0, 0, 0), stroke_width=0.002)
    complem_g = draw.g(stroke=svgwrite.rgb(0, 0, 255), stroke_width=0.002)
    for (i, j), r in cut_ratios.items():
        for uv_i, uv_j in match[i, j]:
            coord_i, coord_j = uv_coords[uv_i], uv_coords[uv_j]
            cut_point = point_on_seg(coord_j, coord_i, r)
            pat_g.add(draw.line(coord_i, cut_point))
            if len(match[i, j]) == 2 or len(connected[undirected(i, j)]) == 1:
                complem_g.add(draw.line(cut_point, coord_j))
    draw.add(pat_g)
    draw.add(complem_g)
    draw.save(True)
