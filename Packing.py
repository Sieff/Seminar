from ParTypes import *


def order_points(points):
    point_array = []
    for point in points:
        point_array.append(point)
    point_array.sort(reverse=True, key=lambda p: p.x + p.y)
    return point_array


def move_point_to_front(point, vertices):
    start_index = 0
    for i in range(len(vertices)):
        if point == vertices[i]:
            if point == vertices[i + 1]:
                start_index = i + 1
            else:
                start_index = i
            break
    return np.roll(vertices, -start_index, axis=0)


def get_lines(points):
    result = []
    for i in range(int(len(points) / 4)):
        line_points, points = points[:4], points[4:]
        start_point = MyPoint(line_points[0][0], line_points[0][1])
        end_point = MyPoint(line_points[-1][0], line_points[-1][1])
        result.append(MyLine(start_point, end_point))
    return np.array(result)


def get_shapes(lines):
    shapes = []
    shape = []
    start = MyPoint(-1, -1)
    for l in lines:
        if l.length() > 0:
            if not shape:
                start = l.start
            if l.end == start:
                shape.append(l)
                shapes.append(shape)
                shape = []
            else:
                shape.append(l)
    return shapes


def get_shape_with_start(start, shapes):
    for shape in shapes:
        for l in shape:
            if l.start == start:
                return shape


def get_index_of_point(point, vertices):
    for i in range(len(vertices)):
        if point == vertices[i]:
            return i


def get_vertices(start, polygon_points):
    lines = get_lines(polygon_points)
    shapes = get_shapes(lines)
    tile_shape = get_shape_with_start(start, shapes)
    vertices = np.array([l.start for l in tile_shape])
    index_of_start = get_index_of_point(start, vertices)
    return np.roll(vertices, -index_of_start)


def length(v):
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def corner_is_left(start, before, after):
    start = start.to_vec2d()
    from_before = start - before.to_vec2d()
    to_after = after.to_vec2d() - start

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


def get_directions(vertices):
    result = []
    for i in range(len(vertices)):
        result.append(corner_dir(vertices, i))
    return np.array(result)


def get_combinations(vertices, target_dir):
    directions = get_directions(vertices)
    parity = 0
    combinations = []
    for i in range(2, len(directions) - 2):
        if directions[i + 1] == directions[i] == target_dir and parity == 0:
            if directions[i - 1] == target_dir:
                if (target_dir == 'l' and vertices[i - 2].y < vertices[i + 2].y) or (
                        target_dir == 'r' and vertices[i - 2].x < vertices[i + 2].x):
                    combinations.append([i, i + 2])
            else:
                combinations.append([i, i + 2])
        if directions[i] == target_dir:
            parity = parity + 1
        else:
            parity = parity - 1
    return np.array(combinations)


def remove_overhangs(vertices, target_dir):
    combinations = get_combinations(vertices, target_dir)
    for i in range(len(combinations)):
        c = combinations[i]
        if target_dir == 'l':
            if vertices[c[0] - 1].y > vertices[c[1]].y:
                vertices = np.append(np.append(vertices[:c[0] - 1], [MyPoint(vertices[c[1]].x, vertices[c[0] - 1].y)]),
                                     vertices[c[1]:])
            elif vertices[c[0] - 1].y < vertices[c[1]].y:
                vertices = np.append(np.append(vertices[:c[0]], [MyPoint(vertices[c[0]].x, vertices[c[1]].y)]),
                                     vertices[c[1] + 1:])
            elif vertices[c[0] - 1].y == vertices[c[1]].y:
                vertices = np.append(vertices[:c[0] - 1], vertices[c[1] + 1:])
        else:
            if vertices[c[0] - 1].x > vertices[c[1]].x:
                vertices = np.append(np.append(vertices[:c[0] - 1], [MyPoint(vertices[c[0] - 1].x, vertices[c[1]].y)]),
                                     vertices[c[1]:])
            elif vertices[c[0] - 1].x < vertices[c[1]].x:
                vertices = np.append(np.append(vertices[:c[0]], [MyPoint(vertices[c[1]].x, vertices[c[0]].y)]),
                                     vertices[c[1] + 1:])
            elif vertices[c[0] - 1].x == vertices[c[1]].x:
                vertices = np.append(vertices[:c[0] - 1], vertices[c[1] + 1:])
        combinations = combinations - (c[1] - c[0])
    return remove_doubles(vertices)


def compare_v_list(v1, v2):
    if len(v1) != len(v2):
        return False
    for i in range(len(v1)):
        if v1[i] != v2[i]:
            return False
    return True


def flip_vertices(vertices):
    return np.flip(np.append(vertices, vertices[0]))[:-1]


def remove_doubles(vertices):
    result = []
    current = MyPoint(-1, -1)
    for v in vertices:
        if v != current:
            result.append(v)
        current = v
    return np.array(result)


def get_greedy_tile(vertices):
    start = vertices[0]
    second = vertices[1]
    if start.x == second.x:
        vertices = flip_vertices(vertices)
    co = 0
    while True:
        co = co + 1
        old_v = vertices.copy()
        vertices = remove_overhangs(vertices, 'l')
        vertices = flip_vertices(vertices)
        vertices = remove_overhangs(vertices, 'r')
        vertices = flip_vertices(vertices)
        if compare_v_list(old_v, vertices):
            break
    return vertices


def get_max_area_vertex(start, vertices):
    max_area = 0
    argmax_area = -1
    for i in range(len(vertices)):
        point = vertices[i]
        area = (point.x - start.x) * (point.y - start.y)
        if area > max_area:
            max_area = area
            argmax_area = i
    return vertices[argmax_area]


def get_greedy_maximal_rect_target(start, tile_points):
    vertices = get_vertices(start, tile_points)
    vertices = get_greedy_tile(vertices)
    return get_max_area_vertex(start, vertices), PossiblePolygon(start, vertices)


def get_tiling_maximal_rect_target(start, tile_points):
    vertices = get_vertices(start, tile_points)
    return get_max_area_vertex(start, vertices), PossiblePolygon(start, vertices)


class Packing:
    def __init__(self, base_rect, ax, scaling):
        self.base_rect = base_rect
        self.base_rect.render(ax, scaling / 2)
        self.ordered_points = order_points(base_rect.pointsSet)
        self.greedy_rectangles, self.greedy_possible_points_polygons, self.greedy_unpacked_space = self._get_greedy_packing(ax, scaling)
        self.tiling_rectangles, self.tiling_possible_points_polygons, self.tiling_unpacked_space = self._get_tile_packing(ax, scaling)
        self._ax = ax
        self._scaling = scaling

    def get_points_creations(self):
        points = []
        for point in self.ordered_points:
            point.render(self._ax)
            points.append(Create(point.mobject))
        return points

    def get_rectangle_transforms(self):
        rectangle_transforms = []
        for idx, packed_rectangle in enumerate(self.greedy_rectangles):
            packed_rectangle.render_transform_base()
            rectangle_transforms.append(Transform(packed_rectangle.transform_base, packed_rectangle.mobject))
        return rectangle_transforms

    def get_possible_points_fades(self):
        possible_points_fadein = []
        possible_points_fadeout = []
        for idx, packed_rectangle in enumerate(self.greedy_rectangles):
            possible_points_fadein.append(FadeIn(self.greedy_possible_points_polygons[idx].mobject))
            possible_points_fadeout.append(FadeOut(self.greedy_possible_points_polygons[idx].mobject))
        return possible_points_fadein, possible_points_fadeout

    def _get_greedy_packing(self, ax, scaling):
        rectangles = []
        possible_points_polygons = []
        tiling = Tiling()
        for point in self.ordered_points:
            total_interesting_rectangle = PackedRectangle(point, MyPoint(1, 1)).render(ax, scaling)
            tile = Difference(total_interesting_rectangle.mobject, tiling.mobject)
            tile_points = ax.p2c(tile.points)
            maximal_rect_target, possible_points_polygon = get_greedy_maximal_rect_target(total_interesting_rectangle.start, tile_points)
            packed_rectangle = PackedRectangle(point, maximal_rect_target).render(ax, scaling)
            tiling.union(packed_rectangle.mobject)

            rectangles.append(packed_rectangle)
            possible_points_polygons.append(possible_points_polygon.render(ax, scaling))

        unpacked_space = Difference(PackedRectangle(MyPoint(0, 0), MyPoint(1, 1)).render(ax, scaling).mobject, tiling.mobject, color=RED, fill_opacity=0.6)
        return rectangles, possible_points_polygons, unpacked_space

    def _get_tile_packing(self, ax, scaling):
        rectangles = []
        possible_points_polygons = []
        tiling = Tiling()
        packing = Tiling()
        for point in self.ordered_points:
            total_interesting_rectangle = PackedRectangle(point, MyPoint(1, 1)).render(ax, scaling)
            tile = Difference(total_interesting_rectangle.mobject, tiling.mobject)
            tile_points = ax.p2c(tile.points)
            maximal_rect_target, possible_points_polygon = get_tiling_maximal_rect_target(
                total_interesting_rectangle.start, tile_points)
            packed_rectangle = PackedRectangle(point, maximal_rect_target).render(ax, scaling)
            tiling.union(tile)
            packing.union(packed_rectangle.mobject)

            rectangles.append(packed_rectangle)
            possible_points_polygons.append(possible_points_polygon.render(ax, scaling))

        unpacked_space = Difference(PackedRectangle(MyPoint(0, 0), MyPoint(1, 1)).render(ax, scaling).mobject,
                                    packing.mobject, color=RED, fill_opacity=0.6)
        return rectangles, possible_points_polygons, unpacked_space
