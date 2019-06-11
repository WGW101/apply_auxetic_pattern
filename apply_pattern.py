from args import parse_args
from parse_obj import parse_file
from topo import get_connected_faces, get_matching_edges, get_matching_vertices
from pattern import get_pattern
from cuts import get_cut_ratios
from plot import plot_pattern

if __name__ == "__main__":
    args = parse_args()
    print("Parsing file '{}'...".format(args.obj_file), end=' ')
    vs, vts, cols, gs, fs, fts = parse_file(args.obj_file)
    print("Done! Model has {} vertices, {} faces in 3d space, {} coordinates and {} faces in UV space.".format(
        len(vs), len(fs), len(vts), len(fts)))

    print("Identifying connected faces...", end=' ')
    con = get_connected_faces(fs)
    print("Done!")

    print("Applying pattern...", end=' ')
    pat, irregs = get_pattern(fs, con)
    print("Done! Pattern was propagated on {} edges (encountered {} irregular face{}).".format(
        len(pat), len(irregs) if len(irregs) > 1 else "no", "" if len(irregs) == 1 else "s"))

    if args.project_to is not None:
        print("Parsing file '{}'...".format(args.project_to), end=' ')
        pvs, vts, _, _, fs, fts = parse_file(args.project_to)
        print("Done! Projected model has {} points and {} faces in UV space.".format(len(vts), len(fts)))

        print("Matching vertices...", end=' ')
        match_v = get_matching_vertices(vs, pvs)
        vs = pvs
        print("Done!")

        print("Transposing pattern...", end=' ')
        pat = {(match_v[i], match_v[j]) for i, j in pat}
        print("Done!")

        print("Updating connected faces...", end=' ')
        con = get_connected_faces(fs)
        print("Done!")

    print("Computing cut lengths...", end=' ')
    rs = get_cut_ratios(vs, cols, fs, con, pat, args.red_len, args.green_len, args.blue_len, args.min_dist)
    print("Done!")

    print("Matching edges from 3d space to uv plane", end=' ')
    match = get_matching_edges(fs, fts)
    print("Done!")

    print("Plotting...", end=' ')
    plot_pattern(args.output, vts, rs, con, match)
    print("Done! SVG file saved as '{}'".format(args.output))
