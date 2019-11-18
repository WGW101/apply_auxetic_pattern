from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from topo import get_all_undirected_edges
from geom import point_on_seg


def preview_pattern_3d(vertices, cut_ratios, irregular_faces):
    fig = pyplot.figure()
    ax: Axes3D = fig.add_subplot(1, 1, 1, projection='3d')

    for (i, j), r in cut_ratios.items():
        vertex_i, vertex_j = vertices[i], vertices[j]
        cut_point = point_on_seg(vertex_j, vertex_i, r)
        ax.plot(*zip(vertex_i, cut_point), color='k')

    for (i, j) in get_all_undirected_edges(irregular_faces):
        vertex_i, vertex_j = vertices[i], vertices[j]
        ax.plot(*zip(vertex_i, vertex_j), color='r')

    pyplot.show()
