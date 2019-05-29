import svgwrite
from topo import undirected
from geom import point_on_seg


def plot_pattern(file_path, uv_coords, cut_ratios, connected, match):
    draw = svgwrite.Drawing(file_path, (1200, 1200), profile="tiny")
    u_offset = min(u for u, v in uv_coords)
    v_offset = min(v for u, v in uv_coords)
    width = max(u for u, v in uv_coords) - u_offset
    height = max(v for u, v in uv_coords) - v_offset
    draw.viewbox(u_offset, v_offset, width, height)
    pat_g = draw.g(stroke=svgwrite.rgb(0, 0, 0), stroke_width=width / 120)
    complem_g = draw.g(stroke=svgwrite.rgb(0, 0, 255), stroke_width=width / 120)
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
