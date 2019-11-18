#!/usr/bin/env python3

from args import parse_args
from parse_obj import parse_file
from topo import get_connected_faces
from pattern import get_pattern
from cuts import get_cut_ratios
from preview_3d import preview_pattern_3d

if __name__ == "__main__":
    args = parse_args()
    print("Parsing file '{}'...".format(args.obj_file), end=' ')
    vertices, uv_coords, colors, groups, faces, uv_faces = parse_file(args.obj_file)
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

    print("Computing cut lengths...", end=' ')
    cut_ratios = get_cut_ratios(vertices, colors, faces, connected_faces, pattern,
                                args.red_len, args.green_len, args.blue_len, args.min_dist)
    print("Done!")

    preview_pattern_3d(vertices, cut_ratios, irregular_faces)
