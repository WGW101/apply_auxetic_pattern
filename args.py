from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="")
    parser.add_argument("obj_file", help="")
    parser.add_argument("--project-to", "-p", help="")
    parser.add_argument("--output", "-o", help="")
    parser.add_argument("--red-len", "-r", type=float, default=3, help="")
    parser.add_argument("--green-len", "-g", type=float, default=4, help="")
    parser.add_argument("--blue-len", "-b", type=float, default=5, help="")
    parser.add_argument("--min-dist", "-d", type=float, default=4, help="")
    return parser.parse_args()
