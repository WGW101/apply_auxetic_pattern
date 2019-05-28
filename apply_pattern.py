from args import parse_args
from parse_obj import parse_file
from topo import get_connected_faces
from pattern import get_pattern
from cuts import get_cut_ratios

if __name__ == "__main__":
    args = parse_args()
    print("Parsing file '{}'...".format(args.obj_file), end=' ')
    vs, vts, cols, gs, fs, fts = parse_file(args.obj_file)
    print("Done! Model has {} vertices, {} faces in 3d space.".format(len(vs), len(fs)))

    if args.project_to is not None:
        print("Parsing file '{}'...".format(args.project_to), end=' ')
        pvs, vts, _, _, _, fts = parse_file(args.project_to)
        print("Done! Projected model has {} points and {} faces in UV space.".format(len(vts), len(fts)))

    print("Identifying connected faces...", end=' ')
    cons = get_connected_faces(fs)
    print("Done!")

    print("Applying pattern...", end=' ')
    pat, irregs = get_pattern(fs, cons)
    print("Done! Pattern was propagated on {} edges (encountered {} irregular face{}).".format(
        len(pat), len(irregs) if len(irregs) > 1 else "no", "" if len(irregs) == 1 else "s"))

    print("Computing cut lengths...", end=' ')
    rs = get_cut_ratios(vs, cols, fs, cons, pat, args.min_cut_len, args.cut_len, args.min_dist)
    print("Done!")
