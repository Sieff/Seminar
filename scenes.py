from manim import *
import numpy as np
from ParTypes import *
import math


def order_points(points):
    point_array = []
    for point in points:
        point_array.append(point)
    point_array.sort(reverse=True, key=lambda p: p.x + p.y)
    return point_array


def get_vertices(start, polygon_points):
    # Move start point to front
    polygon_points = np.roll(polygon_points, 2, axis=0)
    start_index = 0
    for i in range(polygon_points.shape[0]):
        if start == MyPoint(polygon_points[i][0], polygon_points[i][1]):
            if start == MyPoint(polygon_points[i + 1][0], polygon_points[i + 1][1]):
                start_index = i + 1
            else:
                start_index = i
            break
    polygon_points = np.roll(polygon_points, -start_index, axis=0)

    # Get vertices
    first_point, polygon_points = polygon_points[0], polygon_points[1:]
    current_point = MyPoint(first_point[0], first_point[1])
    vertices = [current_point]
    for point in polygon_points:
        if current_point != MyPoint(point[0], point[1]):
            current_point = MyPoint(point[0], point[1])
        elif MyPoint(point[0], point[1]) == start:
            break
        else:
            vertices.append(MyPoint(point[0], point[1]))
            current_point = MyPoint(point[0], point[1])
    return vertices


def angle(v1, v2):
    # return -math.degrees(math.asin((v1[0] * v2[1] - v1[1] * v2[0])/(length(v1)*length(v2))))
    cosTh = np.dot(v1, v2)
    sinTh = np.cross(v1, v2)
    return np.rad2deg(np.arctan2(sinTh, cosTh))


def length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def corner_is_left(start, before, after):
    start = start.to_vec()
    from_before = start - before.to_vec()
    to_after = after.to_vec() - start

    to_before_angle = angle(UP[:2], from_before) % 360
    to_after_angle = angle(UP[:2], to_after) % 360
    return (to_after_angle - to_before_angle) % 360 < 180


def corner_dir(vertices, i):
    if i + 1 == len(vertices):
        is_left_corner = corner_is_left(vertices[i], vertices[i - 1], vertices[0])
    else:
        is_left_corner = corner_is_left(vertices[i], vertices[i - 1], vertices[i + 1])

    if is_left_corner:
        return 'l'
    else:
        return 'r'


def remove_doubles(vertices):
    current = vertices[0]
    result = np.array([current])
    for i in range(1, len(vertices)):
        if vertices[i] != current:
            result = np.append(result, vertices[i])
        current = vertices[i]
    if result[0] == result[-1]:
        return result[:-1]
    else:
        return result


def remove_overhangs(vertices, target_dir):
    if target_dir == 'l':
        counter_dir = 'r'
    else:
        counter_dir = 'l'
    combine_vertices = []
    current_dir = ''
    for i in range(2, len(vertices) - 2):
        dir = corner_dir(vertices, i)
        if current_dir == dir == target_dir:
            inner_current_dir = ''
            for j in range(i + 1, len(vertices)):
                inner_dir = corner_dir(vertices, j)
                if inner_current_dir == inner_dir == counter_dir:
                    combine_vertices.append([i - 1, j - 1])
                    break
                if inner_current_dir == inner_dir == target_dir:
                    break
                inner_current_dir = inner_dir
        current_dir = dir
    combine_vertices = np.array(combine_vertices)
    for i in range(len(combine_vertices)):
        c = combine_vertices[i]
        if target_dir == 'l':
            vertices = np.append(np.append(vertices[:c[0]], [MyPoint(vertices[c[0]].x, vertices[c[1]].y)]),
                                 vertices[c[1] + 1:])
        else:
            vertices = np.append(np.append(vertices[:c[0]], [MyPoint(vertices[c[1]].x, vertices[c[0]].y)]),
                                 vertices[c[1] + 1:])
        combine_vertices = combine_vertices - (c[1] - c[0])
    return vertices


def compare_v_list(v1, v2):
    if len(v1) != len(v2):
        return False
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            return False
    return True


def get_greedy_tile(vertices):
    start = vertices[0]
    second = vertices[1]
    if start.x == second.x:
        vertices = np.flip(vertices)
    while True:
        old_v = vertices.copy()
        vertices = remove_overhangs(vertices, 'l')
        vertices = np.flip(vertices)
        vertices = remove_overhangs(vertices, 'r')
        vertices = np.flip(vertices)
        if compare_v_list(old_v, vertices):
            break
    return vertices


def get_maximal_rect_target(start, tile_points):
    vertices = get_vertices(start, tile_points)
    vertices = remove_doubles(vertices)
    vertices = get_greedy_tile(vertices)
    max_area = 0
    argmax_area = -1
    for i in range(len(vertices)):
        point = vertices[i]
        area = (point.x - start.x) * (point.y - start.y)
        if area > max_area:
            max_area = area
            argmax_area = i
    return vertices[argmax_area]


class PackingGreedyRectangles(Scene):
    def construct(self):
        scaling = 5
        base_rect = BaseRectangle(1, 1)
        base_rect.add_point(0.55, 0.55)
        base_rect.add_point(0.8, 0.7)
        base_rect.add_point(0.7, 0.8)
        base_rect.add_point(0.9, 0.1)
        base_rect.add_point(0.1, 0.9)
        ax = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 2, 1],
            x_length=scaling,
            y_length=scaling,
        )
        self.add(ax)
        base_rect.render(ax, scaling / 2)
        self.add(base_rect.mobject)
        for point in base_rect.pointsSet:
            point.render(ax)
            self.add(point.mobject)
        self.wait()
        ordered_points = order_points(base_rect.pointsSet)
        tiling = Tiling()
        for point in ordered_points:
            packed_rectangle = PackedRectangle(point, MyPoint(1, 1))
            packed_rectangle.render(ax, scaling)
            tile = Difference(packed_rectangle.mobject, tiling.mobject)
            tile_points = ax.p2c(tile.points)
            maximal_rect_target = get_maximal_rect_target(packed_rectangle.start, tile_points)
            packed_rectangle = PackedRectangle(point, maximal_rect_target).render(ax, scaling)
            self.play(Transform(point.mobject, packed_rectangle.mobject))
            tiling.union(packed_rectangle.mobject)

            self.wait()
