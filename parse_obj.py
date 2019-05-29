def parse_file(file_path):
    vertices = []
    uv_coords = []
    colors = []
    groups = []
    faces = []
    uv_faces = []
    with open(file_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            key, *values = line.split()
            if key == 'v':
                vertices.append(tuple(float(val) for val in values[:3]))
            elif key == 'vt':
                uv_coords.append(tuple(float(val) for val in values[:2]))
            elif key == '#MRGB':  # Special key for polypaint (Zbrush)
                colors.extend(tuple(int(values[0][i + j:i + j + 2], 16) for j in range(0, 8, 2))
                              for i in range(0, len(values[0]), 8))
            elif key == 'g':
                groups.append(len(faces))
            elif key == 'f':
                vs, *others = zip(*(val.split('/') for val in values))
                faces.append(tuple(int(v) - 1 for v in vs))
                if len(others) == 1:
                    uv_faces.append(tuple(int(v) - 1 for v in others[0]))
    if abs(max(vertex[2] for vertex in vertices)) < 0.0001:  # 2d object
        uv_coords = [vertex[:2] for vertex in vertices]
        uv_faces = faces.copy()
    return vertices, uv_coords, colors, groups, faces, uv_faces
