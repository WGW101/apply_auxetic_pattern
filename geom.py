from math import sqrt


def dot(v0, v1, v2):
    return sum((x2 - x0) * (x1 - x0) for x0, x1, x2 in zip(v0, v1, v2))


def dist(v0, v1):
    return sqrt(dot(v0, v1, v1))


def cos_angle(v0, v1, v2):
    return dot(v0, v1, v2) / (dist(v0, v1) * dist(v0, v2))


def point_on_seg(v0, v1, r):
    return tuple(x0 + r * (x1 - x0) for x0, x1 in zip(v0, v1))
