from geom import dist


def get_edges(face):
    return face[0:2], face[1:3], (face[2], face[0])


def undirected(i, j):
    return (i, j) if i < j else (j, i)


def get_opposing_vertex(face, i, j):
    for v in face:
        if v != i and v != j:
            return v


def get_connected_faces(faces):
    con = {}
    for f, face in enumerate(faces):
        for i, j in get_edges(face):
            e = (i, j) if i < j else (j, i)
            if e in con:
                con[e].add(f)
            else:
                con[e] = {f}
    return con


def get_matching_edges(faces, uv_faces):
    match = {}
    for face, uv_face in zip(faces, uv_faces):
        for (i, j), (uv_i, uv_j) in zip(get_edges(face), get_edges(uv_face)):
            if (i, j) in match:
                match[i, j].add((uv_i, uv_j))
                match[j, i].add((uv_j, uv_i))
            else:
                match[i, j] = {(uv_i, uv_j)}
                match[j, i] = {(uv_j, uv_i)}
    return match


def get_matching_vertices(vertices, others):
    return [min((dist(vertex, other), v) for v, other in enumerate(others))[1] for vertex in vertices]
