from math import sqrt
from topo import undirected, get_opposing_vertex
from geom import dist, cos_angle


def get_cut_ratios(vertices, colors, faces, connected, pattern, min_len, max_len, min_dist):
    ratios = {}
    for (i, j) in pattern:
        vi, vj = vertices[i], vertices[j]
        l = (colors[j][2] + colors[j][3]) / 510 * (max_len - min_len) + min_len
        for f in connected[undirected(i, j)]:
            a = cos_angle(vj, vi, vertices[get_opposing_vertex(faces[f], i, j)])
            if a > 0:
                l = max(l, min_dist / sqrt(1 - a ** 2))
        ratios[i, j] = l / dist(vi, vj)
    return ratios
