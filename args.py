from argparse import ArgumentParser
import os.path


def parse_args():
    parser = ArgumentParser(description="Script to apply auxetic pattern to a 3D mesh")
    parser.add_argument("obj_file",
                        help="Path to the input .obj file")
    parser.add_argument("--project-to", "-p",
                        help="Optional path to another .obj file to project to other uv coordinates")
    parser.add_argument("--output", "-o",
                        help="Output file name. Uses the input file name with .svg extension by default")
    parser.add_argument("--red-len", "-r", type=float, default=3,
                        help="Minimum material left on an edge with a vertex painted in red")
    parser.add_argument("--green-len", "-g", type=float, default=4,
                        help="Minimum material left on an edge with a vertex painted in green")
    parser.add_argument("--blue-len", "-b", type=float, default=5,
                        help="Minimum material left on an edge with a vertex painted in blue")
    parser.add_argument("--min-dist", "-d", type=float, default=4,
                        help="Minimum orthogonal distance between the end of a cut and any adjacent edge")
    args = parser.parse_args()
    if args.output is None:
        args.output = os.path.splitext(args.obj_file)[0] + '.svg'
    return args
