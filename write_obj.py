from u3d_properties import format_properties
from itertools import chain


def format_vertices(vertices, key="v "):
    return '\n'.join(key + ' '.join(str(x) for x in vert) for vert in vertices)


def format_colors(colors):
    return '\n'.join("#MRGB " + ''.join(format(c, "0>2x") for c in chain.from_iterable(colors[i:i+64]))
                     for i in range(0, len(colors), 64))


def format_faces(groups, faces, uv_faces):
    grp_it = iter(groups)
    g = next(grp_it, -1)
    lines = []
    for f, (face, uv_face) in enumerate(zip(faces, uv_faces)):
        if f == g:
            lines.append("g " + str(g))
            g = next(grp_it, -1)
        lines.append("f " + ' '.join("{}/{}".format(v + 1, vt + 1) for v, vt in zip(face, uv_face)))
    return '\n'.join(lines)


def write_file(vertices, uv_coords, colors, groups, faces, uv_faces, properties, file_path):
    with open(file_path, 'w') as f:
        f.write(format_vertices(vertices, "v ") + '\n')
        if colors:
            f.write(format_colors(colors) + '\n')
        f.write(format_vertices(uv_coords, "vt ") + '\n')
        f.write(format_faces(groups, faces, uv_faces) + '\n')
        if properties:
            f.write("#U3DPROPERTIES_02" + format_properties(properties) + '\n')
