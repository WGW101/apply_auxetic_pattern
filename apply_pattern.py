#!/usr/bin/env python3

from args import parse_args
from parse_obj import parse_file
from topo import get_connected_faces, get_matching_edges, get_matching_vertices
from pattern import get_pattern, reverse_pattern
from cuts import get_cut_ratios
from plot import plot_pattern

if __name__ == "__main__":
    args = parse_args()
    print("Parsing file '{}'...".format(args.obj_file), end=' ')
    vertices, uv_coords, colors, groups, faces, uv_faces, properties = parse_file(args.obj_file)
    print("Done! Model has {} vertices, {} faces in 3d space, {} coordinates and {} faces in UV space.".format(
        len(vertices), len(faces), len(uv_coords), len(uv_faces)))

    print("Identifying connected faces...", end=' ')
    connected_faces = get_connected_faces(faces)
    print("Done!")

    print("Applying pattern...", end=' ')
    pattern, irregular_faces = get_pattern(faces, connected_faces)
    print("Done! Pattern was propagated on {} edges (encountered {} irregular face{}).".format(
        len(pattern),
        len(irregular_faces) if len(irregular_faces) > 1 else "no",
        "" if len(irregular_faces) == 1 else "s"))
    
    if args.reverse:
        print("Reversing edges in pattern...", end=' ')
        pattern = reverse_pattern(pattern)
        print("Done!")

    if args.project_to is not None:
        print("Parsing file '{}'...".format(args.project_to), end=' ')
        project_vertices, uv_coords, colors, groups, faces, uv_faces, properties = parse_file(args.project_to)
        print("Done! Projection model has {} vertices, {} faces in 3d space,".format(
                len(project_vertices), len(faces))
            + "{} coordinates and {} faces in UV space.".format(
                len(uv_coords), len(uv_faces)))

        print("Matching vertices...", end=' ')
        matching_vertices = get_matching_vertices(vertices, project_vertices)
        vertices = project_vertices
        print("Done!")

        print("Transposing pattern...", end=' ')
        pattern = {(matching_vertices[i], matching_vertices[j]) for i, j in pattern}
        print("Done!")

        print("Updating connected faces...", end=' ')
        connected_faces = get_connected_faces(faces)
        print("Done!")

    print("Computing cut lengths...", end=' ')
    cut_ratios = get_cut_ratios(vertices, colors, faces, connected_faces, pattern,
            args.red_len, args.green_len, args.blue_len, args.min_dist)
    print("Done!")

    print("Matching edges from 3d space to uv plane", end=' ')
    matching_edges = get_matching_edges(faces, uv_faces)
    print("Done!")

    print("Plotting...", end=' ')
    plot_pattern(args.output, uv_coords, faces, uv_faces,
                 cut_ratios, connected_faces, matching_edges, args.tile_scale)
    print("Done! SVG file saved as '{}'".format(args.output))
