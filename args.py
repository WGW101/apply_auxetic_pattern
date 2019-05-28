from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(description="")
    parser.add_argument("obj_file", help="")
    parser.add_argument("--project-to", "-p", help="")
    parser.add_argument("--min-cut-len", "-k", type=float, default=0, help="")
    parser.add_argument("--cut-len", "-l", type=float, default=4, help="")
    parser.add_argument("--min-dist", "-d", type=float, default=4, help="")
    return parser.parse_args()
