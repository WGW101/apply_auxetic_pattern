from parse_obj import parse_file
from write_obj import write_file
from topo import get_surrounding_faces
from collections import namedtuple
import math
from argparse import ArgumentParser


Object3D = namedtuple("Object3D", ["vertices", "uv_coords", "colors", "groups", "faces", "uv_faces", "properties"])


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("--color-range", type=int, nargs=2, default=[0, 255])
    parser.add_argument("--density-range", type=int, nargs=2, default=[0.5, 2])
    parser.add_argument("--output-file", default=None)
    return parser.parse_args()


def main(args):
    dens_min, dens_max = args.density_range
    col_min, col_max = args.color_range

    obj = Object3D(*parse_file(args.input_file))

    if obj.colors:
        density = []
        for face in obj.faces:
            col = sum(obj.colors[v][2] + obj.colors[v][3] for v in face) / 6
            density.append(dens_min + (dens_max - dens_min) * (col_max - col) / (col_max - col_min))
        properties = {"Mesh": {"Maps": {"Density": {"Data": density,
                                                    "DefaultValue": 1.0,
                                                    "MaxValue": 4.0,
                                                    "MinValue": 0.1,
                                                    "PrimType": "Polygon",
                                                    "ScaleType": "Log",
                                                    "Size": 1}}}}
        if args.output_file is None:
            args.output_file = args.input_file
        write_file(*obj[:-1], properties, args.output_file)

    elif obj.properties:
        density = obj.properties["Mesh"]["Maps"]["Density"]["Data"]
        surround = get_surrounding_faces(obj.faces)
        colors = []
        for v, _ in enumerate(obj.vertices):
            dens = sum(density[f] for f in surround[v]) / len(surround[v])
            c = math.floor(col_max - (col_max - col_min) * (dens - dens_min) / (dens_max - dens_min))
            colors.append((255, 255, c, c))
        if args.output_file is None:
            args.output_file = args.input_file
        write_file(*obj[:2], colors, *obj[3:], args.output_file)


if __name__ == "__main__":
    main(parse_args())
