from collections import deque
from topo import get_edges, undirected, get_opposing_vertex


def get_pattern(faces, connected, start_f=None):
    pattern = set()
    irregs = []
    not_explored = set(range(len(faces)))
    while not_explored:
        if start_f is None:
            f0 = not_explored.pop()
        else:
            f0 = start_f
            not_explored.remove(start_f)
            start_f = None
        queue = deque([f0])
        pattern.update(set(get_edges(faces[f0])))
        while queue:
            f1 = queue.popleft()
            for i, j in get_edges(faces[f1]):
                f2 = connected[undirected(i, j)] & not_explored
                if f2:
                    f2 = f2.pop()
                    not_explored.remove(f2)
                    v = get_opposing_vertex(faces[f2], i, j)
                    if (i, j) in pattern:
                        if {(v, j), (i, v)} & pattern:
                            irregs.append((i, j, v))
                        else:
                            pattern.add((j, v))
                            pattern.add((v, i))
                            queue.append(f2)
                    else:  # (j, i) in pattern
                        if {(v, i), (j, v)} & pattern:
                            irregs.append((j, i, v))
                        else:
                            pattern.add((i, v))
                            pattern.add((v, j))
                            queue.append(f2)
    return pattern, irregs


def reverse_pattern(pattern):
    return {(j, i) for (i, j) in pattern}