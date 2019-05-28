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
